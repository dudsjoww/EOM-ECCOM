from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class HorarioDeTrabalho(Base):
    __tablename__ = "horarios_de_trabalho"

    id = Column(Integer, primary_key=True, index=True)
    dia_semana = Column(String, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    tatuadores = relationship("Tatuador", back_populates="horarios")
