from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.todos_os_horarios import TodosOsHorarios
from app.schemas.todos_os_horarios import TodosOsHorariosResponse, TodosOsHorariosBase

router = APIRouter(prefix="/todoshorarios", tags=["horarios"])

@router.post("/", response_model=TodosOsHorariosResponse)
def criar_grupo_horario(horarioSchema: TodosOsHorariosBase, db: Session = Depends(get_db)):
    
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
