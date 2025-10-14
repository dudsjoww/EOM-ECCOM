from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tatuador import Tatuador
from app.schemas.tatuador import TatuadorCreate, TatuadorResponse

router = APIRouter(prefix="/tatuadores", tags=["Tatuadores"])

@router.post("/", response_model=TatuadorResponse)
def criar_tatuador(tatuador: TatuadorCreate, db: Session = Depends(get_db)):
    novo = Tatuador(
        user_id=tatuador.user_id,
        especialidade=tatuador.especialidade,
        ativo=True
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[TatuadorResponse])
def listar_tatuadores(db: Session = Depends(get_db)):
    return db.query(Tatuador).all()
