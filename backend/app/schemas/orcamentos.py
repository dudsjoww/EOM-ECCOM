from pydantic import BaseModel


class OrcamentoBase(BaseModel):
    valor_sessao: float
    duracao_horas: float
    qtd_sessoes: int


class OrcamentoCreate(OrcamentoBase):
    pass


class OrcamentoResponse(OrcamentoBase):
    id: int
    enviado_em: str
    confirmado_cliente: bool

    class Config:
        from_attributes = True  # substitui orm_mode
