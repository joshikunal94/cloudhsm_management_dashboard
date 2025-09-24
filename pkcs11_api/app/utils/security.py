import os
import json
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-32-characters-long")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

def generate_encryption_key():
    """Generate a new encryption key for cookies"""
    return Fernet.generate_key()

def get_encryption_key():
    """Get encryption key from environment or generate one"""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        key = generate_encryption_key()
    return key.encode() if isinstance(key, str) else key

def encrypt_data(data: dict) -> str:
    """Encrypt data for cookie storage"""
    fernet = Fernet(get_encryption_key())
    json_data = json.dumps(data)
    encrypted_data = fernet.encrypt(json_data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str) -> dict:
    """Decrypt data from cookie"""
    try:
        fernet = Fernet(get_encryption_key())
        decrypted_data = fernet.decrypt(encrypted_data.encode())
        return json.loads(decrypted_data.decode())
    except Exception:
        return None

def create_access_token(data: dict):
    """Create JWT token for session"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt