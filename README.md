# Secure Web Messaging (AES-128 Encryption)

A secure, Flask-based messaging node demonstrating robust cryptographic principles, RESTful API architecture, and secure environment variable management.

## 📌 Architecture & Security Features
* **Symmetric Encryption:** Utilizes `cryptography.fernet` (AES-128 in CBC mode) to securely encrypt message payloads before they touch the server's storage layer.
* **Key Management Strategy:** Hardcoded keys are strictly prohibited in this application. The system enforces the use of `.env` files and the `python-dotenv` library to isolate the `FERNET_KEY` from the source code, preventing credential leaks in version control.
* **RESTful API:** Structured backend separating encryption (POST `/api/messages/send`) and decryption (GET `/api/messages/receive`) endpoints.
* **Error Handling:** Graceful handling of `InvalidToken` exceptions to detect corrupted payloads, tampered data, or unauthorized decryption attempts.

## 🚀 Installation & Execution

### Prerequisites
* Python 3.8+

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/SecureMessagingApp.git](https://github.com/your-username/SecureMessagingApp.git)
   cd SecureMessagingApp