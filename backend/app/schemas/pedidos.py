from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from typing import List
from app.schemas.sessao import SessaoResponse
from app.schemas.agendamentos import AgendamentoResponse
from app.schemas.user import UserResponse
from app.schemas.tatuador import TatuadorResponse
from app.schemas.venda_consumivel import VendaConsumivelResponse


class StatusPedido(str, Enum):
    SOLICITADO = "solicitado"
    AGUARDANDO_ORCAMENTO = "aguardando_orcamento"
    AGUARDANDO_CONFIRMACAO = "aguardando_confirmacao"
    CONFIRMADO = "confirmado"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


# 🔹 Base comum
class PedidoBase(BaseModel):
    area_corpo: Optional[str] = None
    tamanho: Optional[str] = None
    imagem_png: Optional[str] = None
    coordenadas: Optional[str] = None
    status: Optional[StatusPedido] = StatusPedido.SOLICITADO
    usuario_id: int
    tatuador_id: Optional[int] = None
    observacao: Optional[str] = None
    agendamento_id: Optional[int] = None
    sessao_id: Optional[int] = None


# 🔹 Para criação
class PedidoCreate(PedidoBase):
    pass


# 🔹 Retorno da API
class PedidoResponse(PedidoBase):
    id: int

    criado_em: datetime
    atualizado_em: datetime
    sessao: Optional[SessaoResponse] = []
    agendamento: Optional[AgendamentoResponse] = "Não agendado"
    usuario: UserResponse
    tatuador: Optional[TatuadorResponse] = None
    venda_consumivel: Optional[List[VendaConsumivelResponse]] = []

    class Config:
        from_attributes = True  # substitui orm_mode
