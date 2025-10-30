from pydantic import BaseModel
from typing import Optional, List
from app.schemas.todos_os_horarios import AllHoursResponse


# Base - comum a todos
class TatuadorBase(BaseModel):
    especialidade: Optional[str] = None
    ativo: Optional[bool] = True
    capacidade_diaria: Optional[int] = 5
    preferencia_turno: Optional[str] = "Integral"  # manhã, tarde, noite


# Schema de criação (entrada)
class TatuadorCreate(TatuadorBase):
    usuario_id: int  # FK obrigatória na criação


# Schema de resposta (saída)
class TatuadorResponse(TatuadorBase):
    id: int
    usuario_id: int
    todos_os_horarios: List[AllHoursResponse] = []

    class Config:
        from_attributes = True
