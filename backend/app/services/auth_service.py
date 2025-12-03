from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt
import uuid

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.config import settings
from app.security import verify_password, hash_password, create_access_token


class AuthService:
    ACCESS_EXPIRE_MIN = 15  # 15 min padrão
    REFRESH_DAYS = 7  # sem remember-me
    REFRESH_DAYS_REMEMBER = 30  # com remember-me

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # 1. Autenticar usuário
    # -------------------------
    def authenticate(self, email: str, password: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
            )

        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuário desativado"
            )

        return user

    # -------------------------
    # 2. Criar refresh token
    # -------------------------
    def create_refresh(self, user_id: int, remember: bool) -> RefreshToken:
        duration = self.REFRESH_DAYS_REMEMBER if remember else self.REFRESH_DAYS

        token_str = str(uuid.uuid4()) + "." + str(uuid.uuid4())

        refresh = RefreshToken(
            user_id=user_id,
            token=token_str,
            expiracao=datetime.utcnow() + timedelta(days=duration),
            remember_me=remember,
            valido=True,
        )

        self.db.add(refresh)
        self.db.commit()
        self.db.refresh(refresh)

        return refresh

    # -------------------------
    # 3. Login completo
    # -------------------------
    def login(self, email: str, password: str, remember: bool):
        user = self.authenticate(email, password)

        access = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=self.ACCESS_EXPIRE_MIN),
        )

        refresh = self.create_refresh(user.id, remember)

        return {
            "access_token": access,
            "refresh_token": refresh.token,
            "token_type": "bearer",
        }

    # -------------------------
    # 4. Validar refresh token
    # -------------------------
    def validate_refresh(self, refresh_token: str) -> RefreshToken:
        token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token == refresh_token, RefreshToken.valido == True)
            .first()
        )

        if not token:
            raise HTTPException(401, "Refresh token inválido ou revogado")

        if token.expiracao < datetime.utcnow():
            token.valido = False
            self.db.commit()
            raise HTTPException(401, "Refresh token expirado")

        return token

    # -------------------------
    # 5. Gerar novo access token
    # -------------------------
    def rotate_access(self, refresh_token: str):
        token = self.validate_refresh(refresh_token)

        new_access = create_access_token(
            data={"sub": str(token.user_id)},
            expires_delta=timedelta(minutes=self.ACCESS_EXPIRE_MIN),
        )

        return {"access_token": new_access, "token_type": "bearer"}

    # -------------------------
    # 6. Logout → revoga refresh
    # -------------------------
    def logout(self, refresh_token: str):
        token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token == refresh_token, RefreshToken.valido == True)
            .first()
        )

        if token:
            token.valido = False
            self.db.commit()

        return {"detail": "Logout realizado"}

    # -------------------------
    # 7. Logout global (todas sessões)
    # -------------------------
    def logout_all(self, user_id: int):
        tokens = (
            self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()
        )

        for t in tokens:
            t.valido = False

        self.db.commit()
        return {"detail": "Todas as sessões foram encerradas"}
