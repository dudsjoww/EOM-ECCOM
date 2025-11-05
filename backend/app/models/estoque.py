from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, index=True)
    nome_item = Column(String, nullable=False)
    quantidade = Column(String, nullable=False)
    custo_unitario = Column(Float, nullable=False)
    preco_venda = Column(Float)
    ativo = Column(Boolean, default=True)  # 1 para ativo, 0 para inativo
    passivo = Column(Boolean, default=False)  # 1 para ativo, 0 para inativo
    marca = Column(String(100))
    descricao = Column(String)
    # TODO definir tamanho adequado para unidade_medida, dependendo do uso
    unidade_medida = Column(String(50))
    criado_em = Column(Date, default=datetime.now())
    atualizado_em = Column(Date, default=datetime.now(), onupdate=datetime.now())

    venda_consumivel = relationship("Venda_Consumivel", back_populates="estoque")
