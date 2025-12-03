from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.auth_service import AuthService
from app.core.database import get_db
from sqlalchemy.orm import Session


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rotas públicas não precisam validar
        public_paths = ["/auth/login", "/auth/refresh", "/auth/google"]
        if request.url.path in public_paths:
            return await call_next(request)

        # Pega o token do header
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Token ausente")

        token = token.replace("Bearer ", "")

        # Valida
        try:
            # Abre sessão do DB
            db: Session = next(get_db())
            AuthService.check_access_token(token, db)
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        return await call_next(request)
