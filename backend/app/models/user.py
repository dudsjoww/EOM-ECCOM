from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from app.models.pedidos import Pedido  # ⚠️ precisa existir

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    ativo = Column(Boolean, default=True)  # 1 para ativo, 0 para inativo

    # relacionamento com tatuador
    tatuador = relationship("Tatuador", back_populates="usuario", uselist=False)

    pedidos = relationship("Pedido", back_populates="usuario")
