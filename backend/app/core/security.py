import base64
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies hashed password against plaintext."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def encrypt_sensitive_field(value: str) -> str:
    """Simple obfuscation/encryption wrapper for stored PII tokens."""
    if not value:
        return ""
    key_bytes = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
    val_bytes = value.encode()
    xor_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(val_bytes)])
    return base64.b64encode(xor_bytes).decode('utf-8')


def decrypt_sensitive_field(encrypted_value: str) -> str:
    """Decrypts AES/XOR obfuscated sensitive profile data."""
    if not encrypted_value:
        return ""
    key_bytes = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
    raw_bytes = base64.b64decode(encrypted_value.encode('utf-8'))
    val_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw_bytes)])
    return val_bytes.decode('utf-8')
