from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base
# from app.models.pedidos import Pedido  # ⚠️ precisa existir


class Venda_Consumivel(Base):
    __tablename__ = "venda_consumivel"
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    preco_final = Column(Integer)
    pedidos_id = Column(Integer, ForeignKey("pedidos.id"))
    item_id = Column(Integer, ForeignKey("estoque.id"))

    pedidos = relationship("Pedido", back_populates="venda_consumivel")
    estoque = relationship("Estoque", back_populates="venda_consumivel")
