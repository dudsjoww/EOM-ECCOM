from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import uuid

from app.models.user import User
from app.models.tatuador import Tatuador
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
        access_token = create_access_token(
            data={"sub": str(user.id), "ref": int(refresh.id)},
            expires_delta=timedelta(minutes=self.ACCESS_EXPIRE_MIN),
        )

        return {
            "access_token": access_token,
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
        role = self.identify_role(refresh_token.user_id)
        new_access = create_access_token(
            data={
                "sub": str(refresh_token.user_id),
                "ref": int(refresh_token.id),
                "role": str(role),
            },
            expires_delta=timedelta(minutes=self.ACCESS_EXPIRE_MIN),
        )

        return {"access_token": new_access, "token_type": "bearer"}

    # -------------------------
    # 6. Logout → revoga refresh
    # -------------------------
    def logout(self, token):
        decodedToken = self.decodeJWT(token)
        ref_id = decodedToken.get("ref")

        token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.id == ref_id and RefreshToken.valido)
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

    def decodeJWT(self, token, verify=True):
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": verify},
        )

    # -------------------------
    # 8. Checar access token (middleware)

    def check_access_token(self, token: str):
        try:
            # Decodifica o JWT
            access_token = self.decodeJWT(token, True)

            user_id = access_token.get("sub")
            self.validate_user(user_id)
            ref_id = access_token.get("ref")

            refresh_token = self.validate_refresh(ref_id)
            if not user_id or not ref_id:
                raise HTTPException(401, "Token inválido")
            newToken = self.rotate_access(refresh_token)
            return newToken

        except ExpiredSignatureError:
            payload = self.decodeJWT(token, False)
            ref_id = payload.get("ref")
            user_id = payload.get("sub")

            self.validate_user(user_id)

            token = self.validate_refresh(ref_id)
            if token:
                newToken = self.rotate_access(token)
                return newToken
                # TODO: Fazer uma função retroativo após fazer o navegador receber o header automáticamente
            else:
                raise HTTPException(401, "Token Refresh não encontrado")

        except JWTError:
            raise HTTPException(401, "Token inválido ou expirado teste")

    def identify_role(self, user_id: int) -> str:
        user = self.validate_user(user_id)
        worker = self.validate_worker(user_id)

        if worker.admin:
            return "admin"
        elif worker:
            return "artist"
        elif user:
            return "client"

    def validate_user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(401, "Usuário não encontrado")

        if not user.ativo:
            raise HTTPException(403, "Usuário desativado")
        return user

    def validate_worker(self, user_id: int) -> User:
        worker = self.db.query(Tatuador).filter(Tatuador.user_id == user_id).first()

        if not worker:
            raise HTTPException(401, "Tatuador não encontrado")
        elif not worker.ativo:
            raise HTTPException(403, "Tatuador desativado")
        return worker
