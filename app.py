import os
import sys
import requests
from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# .env dosyasındaki şifreleri güvenle yükle
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "guvenli_degilse_bunu_kullan")

# AES-128 (Fernet) Anahtarını Çek
ENCRYPTION_KEY = os.getenv("FERNET_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("KRİTİK HATA: FERNET_KEY .env dosyasında bulunamadı!")

cipher_suite = Fernet(ENCRYPTION_KEY.encode('utf-8'))

# Port ve Hedef Ayarları (Terminalden okunur)
MY_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
TARGET_PORT = 5002 if MY_PORT == 5001 else 5001
NODE_NAME = "NODE ALPHA (Port: 5001)" if MY_PORT == 5001 else "NODE BETA (Port: 5002)"

# Gelen mesajların tutulacağı geçici bellek
inbox_database = []

@app.route('/')
def index():
    return render_template('index.html', my_name=NODE_NAME, my_port=MY_PORT, target_port=TARGET_PORT)

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.get_json()
    raw_text = data.get('message')
    
    if not raw_text:
        return jsonify({"status": "error", "message": "Boş mesaj gönderilemez."}), 400

    # 1. Mesajı AES ile Şifrele
    encrypted_payload = cipher_suite.encrypt(raw_text.encode('utf-8')).decode('utf-8')
    
    # 2. Şifreli paketi diğer Node'a fırlat
    target_url = f"http://127.0.0.1:{TARGET_PORT}/api/receive"
    try:
        requests.post(target_url, json={"payload": encrypted_payload}, timeout=3)
        return jsonify({"status": "success", "encrypted": encrypted_payload})
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "error", "message": f"HATA: Karşı ağ ({TARGET_PORT}) kapalı veya ulaşılamıyor."}), 503

@app.route('/api/receive', methods=['POST'])
def receive_message():
    data = request.get_json()
    encrypted_payload = data.get('payload')
    
    try:
        # Gelen şifreli paketi çöz (Eğer anahtarlar eşleşiyorsa)
        decrypted_text = cipher_suite.decrypt(encrypted_payload.encode('utf-8')).decode('utf-8')
        inbox_database.append({
            "status": "GÜVENLİ", 
            "content": decrypted_text, 
            "raw_payload": encrypted_payload[:25] + "..."
        })
    except Exception:
        # Anahtar yanlışsa veya paket bozulmuşsa
        inbox_database.append({
            "status": "TEHLİKE!", 
            "content": "[DEŞİFRE EDİLEMEDİ - YETKİSİZ ERİŞİM VEYA BOZUK VERİ]", 
            "raw_payload": encrypted_payload[:25] + "..."
        })
        
    return jsonify({"status": "ok"})

@app.route('/api/inbox', methods=['GET'])
def get_inbox():
    return jsonify(inbox_database)

if __name__ == '__main__':
    print(f"\\n{'='*40}")
    print(f" {NODE_NAME} AKTİF")
    print(f" HEDEF AĞ: 127.0.0.1:{TARGET_PORT}")
    print(f"{'='*40}\\n")
    app.run(host='127.0.0.1', port=MY_PORT, debug=False)