from pydantic import BaseModel
from typing import Optional

# Dados básicos (base para os outros)
class TatuadorBase(BaseModel):
    nome: str
    especialidade: Optional[str] = None
    horarios_id: Optional[int] = None

# Dados de criação (input)
class TatuadorCreate(TatuadorBase):
    pass  # se não houver campos extras no create

# Dados de retorno (output)
class TatuadorResponse(TatuadorBase):
    id: int

    class Config:
        from_attributes = True  # antes era orm_mode = True
