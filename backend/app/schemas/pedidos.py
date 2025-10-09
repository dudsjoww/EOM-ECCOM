from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class StatusPedido(str, Enum):
    SOLICITADO = "solicitado"
    AGUARDANDO_ORCAMENTO = "aguardando_orcamento"
    AGUARDANDO_CONFIRMACAO = "aguardando_confirmacao"
    CONFIRMADO = "confirmado"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


# 🔹 Base comum
class PedidoBase(BaseModel):
    local_tatuagem: str
    tamanho_cm: Optional[float] = None
    imagem_png: Optional[str] = None
    coordenadas: Optional[str] = None


# 🔹 Para criação
class PedidoCreate(PedidoBase):
    usuario_id: int
    tatuador_id: Optional[int] = None


# 🔹 Retorno da API
class PedidoResponse(PedidoBase):
    id: int
    usuario_id: int
    tatuador_id: Optional[int]
    custo_base: Optional[float]
    valor_total: Optional[float]
    status: StatusPedido
    data_agendamento: Optional[datetime]
    data_criacao: datetime

    class Config:
        from_attributes = True  # substitui orm_mode
