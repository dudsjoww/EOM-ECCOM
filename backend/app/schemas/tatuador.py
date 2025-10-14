from pydantic import BaseModel
from typing import Optional,List
from app.schemas.todos_os_horarios import AllHoursResponse

# Base - comum a todos
class TatuadorBase(BaseModel):
    especialidade: Optional[str] = None
    ativo: Optional[bool] = True

# Schema de criação (entrada)
class TatuadorCreate(TatuadorBase):
    user_id: int  # FK obrigatória na criação

# Schema de resposta (saída)
class TatuadorResponse(TatuadorBase):
    id: int
    user_id: int
    todos_os_horarios: List[AllHoursResponse] = []
    class Config:
        from_attributes = True