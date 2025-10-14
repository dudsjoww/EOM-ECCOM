from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.todos_os_horarios import TodosOsHorarios

class HorarioDeTrabalho(Base):
    __tablename__ = "horarios_de_trabalho"
    
    id = Column(Integer, primary_key=True, index=True)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    observacao = Column(String, nullable=True)

    todos_os_horarios = relationship("TodosOsHorarios", back_populates="horario")
