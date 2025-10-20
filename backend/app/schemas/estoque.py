from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime



# Base - comum a todos
class EstoqueBase(BaseModel):
    nome_item: str
    quantidade: int
    custo_unitario: float
    preco_venda: Optional[float] = None
    ativo: Optional[bool] = True
    passive: Optional[bool] = False
    marca : Optional[str] = None
    descricao : Optional[str] = None
    unidade_medida: Optional[str] = None

    @validator('preco_venda', pre=True)
    def calcular_preco_venda(cls, v, values):
        if v is None:
            return values['custo_unitario'] * 1.2
        return v

# Schema de criação (entrada)
class EstoqueCreate(EstoqueBase):
    pass
# Schema de resposta (saída)
class EstoqueResponse(EstoqueBase):
    id: int
    data_registro: Optional[datetime] 