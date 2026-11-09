# Secure Web Messaging (AES-128 P2P Encryption)

A secure, Flask-based dual-node peer-to-peer (P2P) messaging application demonstrating symmetric cryptography (`cryptography.fernet`), RESTful API communication, and secure environment variable management.

## 📌 Architecture & Security Features
* **Symmetric Encryption:** Utilizes `cryptography.fernet` (AES-128 in CBC mode with HMAC authentication) to encrypt message payloads before transmission between nodes.
* **Key Management Strategy:** Hardcoded keys are strictly avoided. The system loads `FERNET_KEY` and `SECRET_KEY` from `.env` using `python-dotenv`, isolating secrets from source control.
* **Dual-Node P2P Architecture:** Supports running two independent nodes (**Node Alpha** on port `5001` and **Node Beta** on port `5002`) that exchange encrypted payloads via `/api/send`, `/api/receive`, and `/api/inbox`.
* **Tamper Detection:** Automatically catches invalid tokens or mismatched keys, flagging unauthorized or corrupted payloads in the inbox.

## 🚀 Installation & Execution

### Prerequisites
* Python 3.8+

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Firatdondar/SecureMessagingApp.git
   cd SecureMessagingApp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   *(Ensure `FERNET_KEY` in `.env` contains a valid 32-byte URL-safe base64-encoded Fernet key, which you can generate via `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`).*

4. Start both nodes in separate terminals:
   ```bash
   # Terminal 1 (Node Alpha - Port 5001)
   python app.py 5001

   # Terminal 2 (Node Beta - Port 5002)
   python app.py 5002
   ```
5. Open `http://127.0.0.1:5001` and `http://127.0.0.1:5002` in your browser to exchange encrypted messages.
