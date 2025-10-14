from pydantic import BaseModel
from typing import List
from app.schemas.horarios import HorarioResponse

class TodosOsHorariosBase(BaseModel):
    tatuador_id: int
    horario_id: int

class TodosOsHorariosResponse(TodosOsHorariosBase):
    id: int
    horario: HorarioResponse  # 👈 inclui o objeto de horário completo

    class Config:
        from_attributes = True

class AllHoursResponse(BaseModel):
    id: int
    horario: HorarioResponse

    class Config:
        from_attributes = True