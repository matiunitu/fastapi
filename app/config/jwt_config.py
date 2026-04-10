from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib

# ─── Configuración JWT ─────────────────────────────────────────────────────────
SECRET_KEY = "supersecretkey_pqrs_2024_$#@!"   # Cambiar en producción
ALGORITHM  = "HS256"
# Token expira en 60 minutos (temporal / sesión corta)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica contraseña usando SHA256"""
    return hashlib.sha256(plain.encode()).hexdigest() == hashed


def hash_password(plain: str) -> str:
    """Hash de contraseña usando SHA256"""
    return hashlib.sha256(plain.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
