from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Tatuador(Base):
    __tablename__ = "tatuadores"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    especialidade = Column(String)
    ativo = Column(Boolean, default=True)
    capacidade_diaria = Column(Integer, default=5)
    preferencia_turno = Column(String, nullable=True)  # manhã, tarde, noite

    # relacionamento com horários de trabalho
    todos_os_horarios = relationship("TodosOsHorarios", back_populates="tatuador")

    # relacionamento com usuario
    usuario = relationship("User", back_populates="tatuador", uselist=False)

    # relacionamento com pedidos
    # pedidos = relationship("Pedido", back_populates="tatuador")
