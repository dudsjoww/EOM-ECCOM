from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Tatuador(Base):
    __tablename__ = "tatuadores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    especialidade = Column(String)
    ativo = Column(Boolean, default=True)  # 1 para ativo, 0 para inativo
    

    # relacionamento com horários de trabalho
    todos_os_horarios = relationship("TodosOsHorarios", back_populates="tatuador", cascade="all, delete-orphan")

    # relacionamento com usuario
    usuario = relationship("User", back_populates="tatuador")

    # relacionamento com pedidos
    pedidos = relationship("Pedido", back_populates="tatuador")
    
