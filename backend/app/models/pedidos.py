from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


# 🔹 Status do pedido (ajuda a controlar o fluxo)
class StatusPedido(str, enum.Enum):
    SOLICITADO = "solicitado"
    AGUARDANDO_ORCAMENTO = "aguardando_orcamento"
    AGUARDANDO_CONFIRMACAO = "aguardando_confirmacao"
    CONFIRMADO = "confirmado"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tatuador_id = Column(Integer, ForeignKey("tatuadores.id"), nullable=True)

    local_tatuagem = Column(String, nullable=False)  # braço, perna, etc.
    tamanho_cm = Column(Float, nullable=True)        # tamanho informado pelo cliente
    imagem_png = Column(String, nullable=True)       # path ou nome do arquivo salvo
    coordenadas = Column(Text, nullable=True)        # JSON com as posições sobre o modelo 3D

    custo_base = Column(Float, nullable=True)
    valor_total = Column(Float, nullable=True)
    status = Column(Enum(StatusPedido), default=StatusPedido.SOLICITADO, nullable=False)

    data_agendamento = Column(DateTime, nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    # 🔗 Relacionamentos
    usuario = relationship("User", back_populates="pedidos")
    tatuador = relationship("Tatuador", back_populates="pedidos")
