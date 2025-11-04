from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    ativo = Column(Boolean, default=True)

    telefone = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.now, nullable=False)

    # relacionamento com tatuador
    tatuador = relationship("Tatuador", back_populates="usuario", uselist=False)
    pedidos = relationship("Pedido", back_populates="usuario")
