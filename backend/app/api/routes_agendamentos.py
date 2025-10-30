from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.agendamentos import Agendamentos
from app.schemas.agendamentos import AgendamentoCreate, AgendamentoResponse

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


@router.post("/", response_model=AgendamentoResponse)
def criar_pedido(AgendamentoSchema: AgendamentoCreate, db: Session = Depends(get_db)):
    novo = Agendamentos(
        data_agendada=AgendamentoSchema.data_agendada,
        hora_inicio=AgendamentoSchema.hora_inicio,
        hora_fim=AgendamentoSchema.hora_fim,
        confirmado_cliente=AgendamentoSchema.confirmado_cliente,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(Agendamentos).all()


@router.get("/{agendamento_id}", response_model=AgendamentoResponse)
def obter_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = (
        db.query(Agendamentos).filter(Agendamentos.id == agendamento_id).first()
    )
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento


@router.delete("/{agendamento_id}", response_model=dict)
def deletar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = (
        db.query(Agendamentos).filter(Agendamentos.id == agendamento_id).first()
    )
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    else:
        db.delete(agendamento)
        db.commit()
        return {"detail": "Agendamento deletado com sucesso"}


@router.put("/{agendamento_id}", response_model=AgendamentoResponse)
def atualizar_agendamento(
    agendamento_id: int,
    AgendamentoSchema: AgendamentoCreate,
    db: Session = Depends(get_db),
):
    agendamento = (
        db.query(Agendamentos).filter(Agendamentos.id == agendamento_id).first()
    )
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    else:
        agendamento.data_agendada = AgendamentoSchema.data_agendada
        agendamento.hora_inicio = AgendamentoSchema.hora_inicio
        agendamento.hora_fim = AgendamentoSchema.hora_fim
        agendamento.confirmado_cliente = AgendamentoSchema.confirmado_cliente

        db.commit()
        db.refresh(agendamento)
        return agendamento
