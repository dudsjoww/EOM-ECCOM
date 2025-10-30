from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Sessao(Base):
    id = Column(Integer, primary_key=True, index=True)
    orcamento_id = Column(Integer, ForeignKey("orcamentos.id"), nullable=False)
    data_sessao = Column(DateTime, nullable=False)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fim = Column(DateTime, nullable=False)
    observacoes = Column(Text, nullable=True)


orcamentos = relationship("Orcamentos", back_populates="sessao")
pedidos = relationship("Pedido", back_populates="sessao")
