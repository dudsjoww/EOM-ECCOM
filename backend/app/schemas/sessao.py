from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class SessaoBase(BaseModel):
    duracao_horas: time
    data_sessao: date
    hora_inicio: time
    hora_fim: time
    orcamento_id: Optional[int]
    observacao: Optional[str] = None


class SessaoCreate(SessaoBase):
    orcamento_id: int


class SessaoResponse(SessaoBase):
    id: int
