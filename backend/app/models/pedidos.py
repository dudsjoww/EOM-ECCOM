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
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tatuador_id = Column(Integer, ForeignKey("tatuadores.id"), nullable=True)

    area_corpo = Column(String, nullable=False)  # braço, perna, etc.
    tamanho = Column(Float, nullable=True)  # tamanho informado pelo cliente
    imagem_png = Column(String, nullable=True)  # path ou nome do arquivo salvo
    coordenadas = Column(Text, nullable=True)  # JSON com as posições sobre o modelo 3D
    observacao = Column(Text, nullable=True)

    criado_em = Column(DateTime, default=datetime.now, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    status = Column(Enum(StatusPedido), default=StatusPedido.SOLICITADO, nullable=False)

    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"), nullable=True)
    sessao_id = Column(Integer, ForeignKey("sessao.id"), nullable=True)

    # 🔗 Relacionamentos
    # usuario = relationship("User", back_populates="pedidos")
    # tatuador = relationship("Tatuador", back_populates="pedidos")
    agendamento = relationship(
        "Agendamentos", back_populates="pedidos", uselist=False
    )  # um-para-um
    # sessao = relationship("Sessao", back_populates="pedidos")
    venda_consumivel = relationship(
        "Venda_Consumivel", back_populates="pedidos"
    )  # um-para-muitos
