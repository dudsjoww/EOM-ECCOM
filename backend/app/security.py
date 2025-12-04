from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

# 🔥 Um único CryptContext global
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# -------------------------------
# 1. Hash de senha
# -------------------------------
def hash_password(password: str) -> str:
    """
    Recebe uma senha pura e devolve o hash bcrypt.
    """
    return pwd_context.hash(password)


# -------------------------------
# 2. Verificar senha
# -------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara senha pura com o hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# 3. Criar access token JWT
# -------------------------------
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Gera um JWT assinado contendo 'exp'.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt
