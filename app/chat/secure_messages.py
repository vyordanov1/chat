import os, base64
from cryptography.fernet import Fernet

SECRET_KEY = str(os.environ.get("FERNET_KEY"))
fernet = Fernet(SECRET_KEY)


def encrypt_text(plain_text: str):
    return fernet.encrypt(plain_text.encode()).decode()


def decrypt_text(encrypted_text: str):
    return fernet.decrypt(encrypted_text.encode()).decode()