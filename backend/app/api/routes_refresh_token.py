from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken

from app.schemas.auth_schemas import (
    SchemaLogin,
    SchemaTokenResponse,
    SchemaRefreshToken,
    SchemaRefreshTokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "SECRET_KEY"  # troque por .env
ALGORITHM = "HS256"

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_minutes: int = 15):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token():
    import secrets

    return secrets.token_urlsafe(64)


@router.post("/login", response_model=SchemaTokenResponse)
def login(payload: SchemaLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.username).first()

    if not user or not pwd.verify(payload.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Criar access token
    access_token = create_access_token({"sub": str(user.id)}, expires_minutes=15)

    # Criar refresh token
    refresh_token_str = create_refresh_token()

    refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expiracao=datetime.utcnow() + timedelta(days=7),
        remember_me=False,
    )

    db.add(refresh)
    db.commit()

    return SchemaTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
    )


@router.post("/login/remember", response_model=SchemaTokenResponse)
def login_remember(payload: SchemaLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.username).first()

    if not user or not pwd.verify(payload.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token({"sub": str(user.id)}, expires_minutes=30)

    refresh_token_str = create_refresh_token()

    refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expiracao=datetime.utcnow() + timedelta(days=30),
        remember_me=True,
    )

    db.add(refresh)
    db.commit()

    return SchemaTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
    )


@router.post("/refresh", response_model=SchemaRefreshTokenResponse)
def refresh_token(payload: SchemaRefreshToken, db: Session = Depends(get_db)):
    token_db = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == payload.refresh_token, RefreshToken.valido == True
        )
        .first()
    )

    if not token_db:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    if token_db.expiracao < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expirado")

    user = db.query(User).filter(User.id == token_db.user_id).first()

    # Rotacionar refresh token (segurança máxima)
    novo_refresh = create_refresh_token()

    token_db.token = novo_refresh  # substitui o antigo
    db.commit()

    access = create_access_token({"sub": str(user.id)})

    return SchemaRefreshTokenResponse(access_token=access)


@router.post("/logout")
def logout(payload: SchemaRefreshToken, db: Session = Depends(get_db)):
    token_db = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == payload.refresh_token)
        .first()
    )

    if token_db:
        token_db.valido = False
        db.commit()

    return {"detail": "Logout realizado com sucesso"}


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"id": user.id, "nome": user.nome, "email": user.email}
