from fastapi import APIRouter, Depends, HTTPException  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # type: ignore
from app.core.database import get_db
from app.models.todos_os_horarios import TodosOsHorarios
from app.schemas.todos_os_horarios import TodosOsHorariosResponse, TodosOsHorariosBase

router = APIRouter(prefix="/todoshorarios", tags=["horarios"])


@router.post("/", response_model=TodosOsHorariosResponse)
def criar_grupo_horario(
    horarioSchema: TodosOsHorariosBase, db: Session = Depends(get_db)
):
    novo = TodosOsHorarios(
        tatuador_id=horarioSchema.tatuador_id,
        horario_id=horarioSchema.horario_id,
    )
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar horário: {str(e)}")


@router.get("/", response_model=list[TodosOsHorariosResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(TodosOsHorarios).all()


@router.get("/{grupo_horario_id}", response_model=TodosOsHorariosResponse)
def obter_grupo_horario(grupo_horario_id: int, db: Session = Depends(get_db)):
    grupo_horario = (
        db.query(TodosOsHorarios).filter(TodosOsHorarios.id == grupo_horario_id).first()
    )
    if not grupo_horario:
        raise HTTPException(status_code=404, detail="Grupo de horário não encontrado")
    return grupo_horario


@router.delete("/{grupo_horario_id}", response_model=dict)
def deletar_grupo_horario(grupo_horario_id: int, db: Session = Depends(get_db)):
    grupo_horario = (
        db.query(TodosOsHorarios).filter(TodosOsHorarios.id == grupo_horario_id).first()
    )
    if not grupo_horario:
        raise HTTPException(status_code=404, detail="Grupo de horário não encontrado")
    else:
        db.delete(grupo_horario)
        db.commit()
        return {"detail": "Grupo de horário deletado com sucesso"}


@router.put("/{grupo_horario_id}", response_model=TodosOsHorariosResponse)
def atualizar_grupo_horario(
    grupo_horario_id: int,
    horarioSchema: TodosOsHorariosBase,
    db: Session = Depends(get_db),
):
    grupo_horario = (
        db.query(TodosOsHorarios).filter(TodosOsHorarios.id == grupo_horario_id).first()
    )
    if not grupo_horario:
        raise HTTPException(status_code=404, detail="Grupo de horário não encontrado")
    else:
        grupo_horario.tatuador_id = horarioSchema.tatuador_id
        grupo_horario.horario_id = horarioSchema.horario_id
        db.commit()
        db.refresh(grupo_horario)
        return grupo_horario
