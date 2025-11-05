from pydantic import BaseModel
from typing import Optional


class VendaConsumivelBase(BaseModel):
    item_id: int
    quantidade: int
    preco_final: Optional[float] = None
    pedidos_id: int


class VendaConsumivelCreate(VendaConsumivelBase):
    pass


class VendaConsumivelResponse(VendaConsumivelBase):
    id: int
