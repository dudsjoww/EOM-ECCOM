from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import time, date, datetime


# Base - comum a todos
class AgendamentoBase(BaseModel):
    data_agendada: date
    hora_inicio: time
    hora_fim: time
    confirmado_cliente : Optional[bool] = False
    observacao: Optional[str] = None

    @field_validator('data_agendada')
    def data_no_passado(cls, v):
        if v < date.today():
            raise ValueError('A data agendada não pode ser no passado.')
        return v
    
    @model_validator(mode='after')
    def hora_fim_maior_que_inicio(self):
        if self.hora_fim <= self.hora_inicio:
            raise ValueError('A hora de fim deve ser maior que a hora de início.')
        return self
    

# Schema de criação (entrada)
class AgendamentoCreate(AgendamentoBase):
    pass
# Schema de resposta (saída)
class AgendamentoResponse(AgendamentoBase):
    id: int
    criado_em: datetime