from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.estoque import Estoque
from app.schemas.estoque import EstoqueCreate, EstoqueResponse
from datetime import datetime

router = APIRouter(prefix="/estoque", tags=["estoque"])

@router.post("/", response_model=EstoqueResponse)
def criar_horario(EstoqueSchema: EstoqueCreate, db: Session = Depends(get_db)):
    

    
    novo = Estoque(
        nome_item=EstoqueSchema.nome_item,
        quantidade=EstoqueSchema.quantidade,
        custo_unitario=EstoqueSchema.custo_unitario,    
        preco_venda=EstoqueSchema.preco_venda ,
        ativo=EstoqueSchema.ativo,
        passive=EstoqueSchema.passive,
        marca=EstoqueSchema.marca,
        descricao=EstoqueSchema.descricao,
        unidade_medida=EstoqueSchema.unidade_medida,
    )
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar item do estoque: {str(e)}")

@router.get("/", response_model=list[EstoqueResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(Estoque).all()
