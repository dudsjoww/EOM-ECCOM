from pydantic import BaseModel
from typing import Optional


class OrcamentoBase(BaseModel):
    valor_sessao: float
    duracao_horas: float
    qtd_sessoes: int
    confirmado_cliente: Optional[bool] = False


class OrcamentoCreate(OrcamentoBase):
    pass


class OrcamentoResponse(OrcamentoBase):
    id: int
    enviado_em: str

    class Config:
        from_attributes = True  # substitui orm_mode
