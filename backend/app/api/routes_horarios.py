from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.horario_de_trabalho import HorarioDeTrabalho
from app.schemas.horarios import HorarioCreate, HorarioResponse

router = APIRouter(prefix="/horarios", tags=["horarios"])


@router.post("/", response_model=HorarioResponse)
def criar_horario(horarioSchema: HorarioCreate, db: Session = Depends(get_db)):
    db_hour = (
        db.query(HorarioDeTrabalho)
        .filter(
            horarioSchema.dia_semana == HorarioDeTrabalho.dia_semana
            and horarioSchema.hora_inicio == HorarioDeTrabalho.hora_inicio
            and horarioSchema.hora_fim == HorarioDeTrabalho.hora_fim
        )
        .first()
    )

    if db_hour:
        raise HTTPException(
            status_code=400, detail=f"Data e horario já cadastrado, db_id: {db_hour.id}"
        )
    else:
        novo = HorarioDeTrabalho(
            dia_semana=horarioSchema.dia_semana,
            hora_inicio=horarioSchema.hora_inicio,
            hora_fim=horarioSchema.hora_fim,
            observacao=horarioSchema.observacao,
        )
        try:
            db.add(novo)
            db.commit()
            db.refresh(novo)
            return novo
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=400, detail=f"Erro ao criar horário: {str(e)}"
            )


@router.get("/", response_model=list[HorarioResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(HorarioDeTrabalho).all()


@router.get("/{horario_id}", response_model=HorarioResponse)
def obter_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = (
        db.query(HorarioDeTrabalho).filter(HorarioDeTrabalho.id == horario_id).first()
    )
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return horario


@router.delete("/{horario_id}", response_model=dict)
def deletar_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = (
        db.query(HorarioDeTrabalho).filter(HorarioDeTrabalho.id == horario_id).first()
    )
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    else:
        db.delete(horario)
        db.commit()
        return {"detail": "Horário deletado com sucesso"}


@router.put("/{horario_id}", response_model=HorarioResponse)
def atualizar_horario(
    horario_id: int, horarioSchema: HorarioCreate, db: Session = Depends(get_db)
):
    horario = (
        db.query(HorarioDeTrabalho).filter(HorarioDeTrabalho.id == horario_id).first()
    )
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    else:
        horario.dia_semana = horarioSchema.dia_semana
        horario.hora_inicio = horarioSchema.hora_inicio
        horario.hora_fim = horarioSchema.hora_fim
        horario.observacao = horarioSchema.observacao
        db.commit()
        db.refresh(horario)
        return horario
