from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


# Base - comum a todos
class EstoqueBase(BaseModel):
    nome_item: str
    quantidade: int
    custo_unitario: float
    preco_venda: Optional[float] = None
    ativo: Optional[bool] = True
    passivo: Optional[bool] = False
    marca: str = None
    descricao: Optional[str] = None
    unidade_medida: str = None

    @field_validator("preco_venda", mode="after")
    def calcular_preco_venda(cls, v, info):
        # Se o preço de venda não for informado, calcular com base no custo
        if v is None:
            custo = info.data.get("custo_unitario")
            if custo is None:
                raise ValueError(
                    "custo_unitario deve ser informado para calcular preco_venda"
                )
            v = custo * 1.2  # margem de 20%
        return round(v, 2)  # Formata para 2 casas decimais


# Schema de criação (entrada)
class EstoqueCreate(EstoqueBase):
    pass


# Schema de resposta (saída)
class EstoqueResponse(EstoqueBase):
    id: int
    criado_em: Optional[datetime]
    atualizado_em: Optional[datetime]


class EstoqueUpdate(BaseModel):
    nome_item: Optional[str] = None
    quantidade: Optional[int] = None
    custo_unitario: Optional[float] = None
    preco_venda: Optional[float] = None
    ativo: Optional[bool] = None
    passivo: Optional[bool] = None
    marca: Optional[str] = None
    descricao: Optional[str] = None
    unidade_medida: Optional[str] = None
