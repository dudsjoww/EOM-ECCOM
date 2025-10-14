from pydantic import BaseModel
from typing import Optional
from datetime import time


# Base - comum a todos
class HorarioBase(BaseModel):
    dia_semana: str
    hora_inicio: time
    hora_fim: time
    observacao: Optional[str] = None

# Schema de criação (entrada)
class HorarioCreate(HorarioBase):
    pass
# Schema de resposta (saída)
class HorarioResponse(HorarioBase):
    id: int