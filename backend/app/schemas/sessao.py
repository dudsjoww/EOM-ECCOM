from pydantic import BaseModel, Optional
from datetime import date, time


class SessaoBase(BaseModel):
    duracao_horas: float
    data_sessao: date
    hora_inicio: time
    hora_fim: time
    observacaoes: Optional[str] = None


class SessaoCreate(SessaoBase):
    pass


class SessaoResponse(SessaoBase):
    id: int
