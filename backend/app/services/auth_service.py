from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import uuid

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.config import settings
from app.security import verify_password, create_access_token


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
            expiracao=datetime.now() + timedelta(days=duration),
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
        refresh = self.create_refresh(user.id, remember)
        access = create_access_token(
            data={"sub": str(user.id), "ref": int(refresh.id)},
            expires_delta=timedelta(minutes=self.ACCESS_EXPIRE_MIN),
        )

        return {
            "access_token": access,
            "refresh_token": refresh.token,
            "token_type": "bearer",
        }

    # -------------------------
    # 4. Validar refresh token
    # -------------------------
    def validate_refresh(self, refresh_token_id: int):
        token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.id == refresh_token_id, RefreshToken.valido)
            .first()
        )

        if not token:
            raise HTTPException(401, "Refresh token inválido ou revogado")

        if token.expiracao < datetime.now():
            token.valido = False
            self.db.commit()
            raise HTTPException(401, "Refresh token expirado")

        return token

    # -------------------------
    # 5. Gerar novo access token
    # -------------------------
    def rotate_access(self, refresh_token: RefreshToken):

        new_access = create_access_token(
            data={"sub": str(refresh_token.user_id), "ref": int(refresh_token.id)},
            expires_delta=timedelta(minutes=self.ACCESS_EXPIRE_MIN),
        )

        return {"access_token": new_access, "token_type": "bearer"}

    # -------------------------
    # 6. Logout → revoga refresh
    # -------------------------
    def logout(self, refresh_token: str):
        token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token == refresh_token, RefreshToken.valido)
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

    # -------------------------
    # 8. Checar access token (middleware)
    def check_access_token(self, token: str, db: Session):
        try:
            # Decodifica o JWT
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

            user_id = payload.get("sub")
            ref_id = payload.get("ref")
            if not user_id or not ref_id:
                raise HTTPException(401, "Token inválido")

            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(401, "Usuário não encontrado")

            if not user.ativo:
                raise HTTPException(403, "Usuário desativado")

            return user

        except ExpiredSignatureError:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                options={"verify_exp": False},
            )
            ref_id = payload.get("ref")
            user_id = payload.get("sub")

            token = self.validate_refresh(ref_id)
            if token:
                return self.rotate_access(token)
            else:
                raise HTTPException(401, "Token Refresh não encontrado")

        except JWTError:
            raise HTTPException(401, "Token inválido ou expirado")
