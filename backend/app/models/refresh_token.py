from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    token = Column(String, unique=True, index=True)  # refresh token criptografado
    expiracao = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    # se o usuário clicou "remember me"
    remember_me = Column(Boolean, default=False)

    # controle de sessão (útil pra revogação)
    valido = Column(Boolean, default=True)

    user = relationship("User", back_populates="tokens")
