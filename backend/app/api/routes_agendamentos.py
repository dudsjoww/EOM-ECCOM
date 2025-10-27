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
        confirmado_cliente=AgendamentoSchema.confirmado_cliente
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(Agendamentos).all()
