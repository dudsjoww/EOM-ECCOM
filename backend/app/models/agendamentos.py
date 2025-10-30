from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    Text,
    Date,
    Time,
    Boolean,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime, date


class Agendamentos(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    data_agendada = Column(Date, nullable=True)
    hora_fim = Column(Time, nullable=True)
    hora_inicio = Column(Time, nullable=True)
    confirmado_cliente = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.now, nullable=False)

    # 🔗 Relacionamentos
    pedidos = relationship("Pedido", back_populates="agendamento")
