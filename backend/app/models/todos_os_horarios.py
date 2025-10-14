# app/models/todos_os_horarios.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class TodosOsHorarios(Base):
    __tablename__ = "todos_os_horarios"

    id = Column(Integer, primary_key=True, index=True)
    tatuador_id = Column(Integer, ForeignKey("tatuadores.id", ondelete="CASCADE"))
    horario_id = Column(Integer, ForeignKey("horarios_de_trabalho.id", ondelete="CASCADE"))

    tatuador = relationship("Tatuador", back_populates="todos_os_horarios")
    horario = relationship("HorarioDeTrabalho", back_populates="todos_os_horarios")
