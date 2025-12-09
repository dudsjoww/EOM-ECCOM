from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.auth_service import AuthService
from app.core.database import get_db
from sqlalchemy.orm import Session


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = [
            "/auth/login",
            "/auth/refresh",
            "/auth/google",
            "/usuarios/",  # <- rota pública para criação
        ]

        # Rota pública? deixa passar
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Pegar Bearer Token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token ausente")

        token = auth_header.replace("Bearer ", "")

        # Validação do token
        db: Session = next(get_db())
        auth = AuthService(db)
        auth.check_access_token(token)

        return await call_next(request)
