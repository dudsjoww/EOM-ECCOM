from pydantic import BaseModel


class VendaConsumivelBase(BaseModel):
    item_id: int
    quantidade: int
    preco_final: int
    pedidos_id: int


class VendaConsumivelCreate(VendaConsumivelBase):
    pass


class VendaConsumivelResponse(VendaConsumivelBase):
    id: int
