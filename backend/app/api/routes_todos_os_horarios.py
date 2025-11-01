from fastapi import APIRouter, Depends, HTTPException  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # type: ignore
from app.core.database import get_db
from app.models.todos_os_horarios import TodosOsHorarios
from app.models.tatuador import Tatuador
from app.models.horario_de_trabalho import HorarioDeTrabalho
from app.schemas.todos_os_horarios import TodosOsHorariosResponse, TodosOsHorariosBase

router = APIRouter(prefix="/todoshorarios", tags=["horarios"])

# TODO: POST não criados utilizando IDs


#
@router.post("/", response_model=TodosOsHorariosResponse)
def criar_grupo_horario(
    horarioSchema: TodosOsHorariosBase, db: Session = Depends(get_db)
):
    item_existe(horarioSchema, db, 0)
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
        db.expire_all()

        return {"detail": "Grupo de horário deletado com sucesso"}


@router.put("/{grupo_horario_id}", response_model=TodosOsHorariosResponse)
def atualizar_grupo_horario(
    grupo_horario_id: int,
    horarioSchema: TodosOsHorariosBase,
    db: Session = Depends(get_db),
):
    item_existe(horarioSchema, db, grupo_horario_id)

    grupo_horario = TodosOsHorarios(
        tatuador_id=horarioSchema.tatuador_id, horario_id=horarioSchema.horario_id
    )
    db.commit()
    db.refresh(grupo_horario)
    return grupo_horario


def item_existe(schema, db, id=0):
    if id:
        if (
            db.query(TodosOsHorarios)
            .filter(TodosOsHorarios.id == id)
            .first()
            .execution_options(populate_existing=True)
        ):
            raise HTTPException(
                status_code=404, detail="Grupo de Horarios não encontrado"
            )

    db_search_horario = (
        db.query(HorarioDeTrabalho)
        .filter(HorarioDeTrabalho.id == schema.horario_id)
        .first()
    )
    db_search_tatuador = (
        db.query(Tatuador).filter(Tatuador.id == schema.tatuador_id).first()
    )
    # Valida se não existe tatuador ou horario
    if not db_search_horario or not db_search_tatuador:
        raise HTTPException(
            status_code=404, detail="Tatuador ou Horario de Trabalho não encontrado"
        )
    # Valida se já existe a relação que solicita
    elif (
        db.query(TodosOsHorarios)
        .filter(
            schema.tatuador_id == TodosOsHorarios.tatuador_id
            and schema.horario_id == TodosOsHorarios.horario_id
        )
        .first()
    ):
        raise HTTPException(status_code=404, detail="Relação já feita")
    else:
        return
