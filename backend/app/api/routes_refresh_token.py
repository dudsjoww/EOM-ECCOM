from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt
from app.services.auth_service import AuthService
from app.core.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.auth import (
    SchemaLogin,
    SchemaTokenResponse,
    SchemaRefreshToken,
    # SchemaRefreshTokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


@router.post("/login", response_model=SchemaTokenResponse)
def loginRoute(payload: SchemaLogin, db: Session = Depends(get_db)):

    auth = AuthService(db)

    tokens = auth.login(payload.email, payload.password, payload.remember_me)
    print(tokens)
    return SchemaTokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
    )


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    auth = AuthService(db)
    print(token)
    auth.logout(token)

    return {"detail": "Logout realizado com sucesso"}


@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    auth = AuthService(db)
    user = auth.check_access_token(token)
    return user
    # return {"id": user.id, "nome": user.nome, "email": user.email}
