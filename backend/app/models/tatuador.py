from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Tatuador(Base):
    __tablename__ = "tatuadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String)
    especialidade = Column(String)

    # relacionamento com horários de trabalho
    horarios_id = Column(Integer, ForeignKey("horarios_de_trabalho.id"))
    horarios = relationship("HorarioDeTrabalho", back_populates="tatuadores")

    # relacionamento com pedidos
    pedidos = relationship("Pedido", back_populates="tatuador")
