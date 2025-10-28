from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class orcamentos(Base):
    __tablename__ = "orcamentos"
    id = Column(Integer, primary_key=True, index=True)

    valor_sessao = Column(Float, nullable=False)
    duracao_horas = Column(Float, nullable=False)
    qtd_sessoes = Column(Integer, nullable=False)
    enviado_em = Column(DateTime, nullable=False)
    confirmado_cliente = Column(Boolean, default=False)

    sessao = relationship("Sessao", back_populates="orcamentos")
