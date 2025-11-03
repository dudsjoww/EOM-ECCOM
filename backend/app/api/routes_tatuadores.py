from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tatuador import Tatuador
from app.models.user import User as Usuario
from app.schemas.tatuador import TatuadorCreate, TatuadorResponse

router = APIRouter(prefix="/tatuadores", tags=["Tatuadores"])


@router.post("/", response_model=TatuadorResponse)
def criar_tatuador(tatuador: TatuadorCreate, db: Session = Depends(get_db)):
    if db.query(Tatuador).filter(Tatuador.usuario_id == tatuador.usuario_id).first():
        raise HTTPException(
            status_code=400, detail="Tatuador já cadastrado para este usuário"
        )
    elif not db.query(Usuario).filter(Usuario.id == tatuador.usuario_id).first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        novo = Tatuador(
            usuario_id=tatuador.usuario_id,
            especialidade=tatuador.especialidade,
            capacidade_diaria=tatuador.capacidade_diaria,
            preferencia_turno=tatuador.preferencia_turno,
            ativo=tatuador.ativo,
        )
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo


@router.get("/", response_model=list[TatuadorResponse])
def listar_tatuadores(db: Session = Depends(get_db)):
    return db.query(Tatuador).all()


@router.get("/{tatuador_id}", response_model=TatuadorResponse)
def obter_tatuador(tatuador_id: int, db: Session = Depends(get_db)):
    tatuador = db.query(Tatuador).filter(Tatuador.id == tatuador_id).first()
    if not tatuador:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    return tatuador


@router.delete("/{tatuador_id}", response_model=dict)
def deletar_tatuador(tatuador_id: int, db: Session = Depends(get_db)):
    tatuador = db.query(Tatuador).filter(Tatuador.id == tatuador_id).first()
    if not tatuador:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    else:
        db.delete(tatuador)
        db.commit()
        db.expire_all()
        return {"detail": "Tatuador deletado com sucesso"}


@router.put("/{tatuador_id}", response_model=TatuadorResponse)
def atualizar_tatuador(
    tatuador_id: int, tatuador: TatuadorCreate, db: Session = Depends(get_db)
):
    tatuador_db = db.query(Tatuador).filter(Tatuador.id == tatuador_id).first()
    if not tatuador_db:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    else:
        tatuador_db.especialidade = tatuador.especialidade
        tatuador_db.capacidade_diaria = tatuador.capacidade_diaria
        tatuador_db.preferencia_turno = tatuador.preferencia_turno
        tatuador_db.ativo = tatuador.ativo

        db.commit()
        db.refresh(tatuador_db)
        return tatuador_db
