from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
from app.schemas.sessao import SessaoResponse


class OrcamentoBase(BaseModel):
    valor_sessao: float
    duracao_horas: time
    qtd_sessoes: int
    confirmado_cliente: Optional[bool] = False


class OrcamentoCreate(OrcamentoBase):
    pass


class OrcamentoResponse(OrcamentoBase):
    id: int
    enviado_em: datetime
    sessao: Optional[list[SessaoResponse]] = []

    class Config:
        from_attributes = True  # substitui orm_mode
