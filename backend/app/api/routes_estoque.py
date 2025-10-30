from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.estoque import Estoque
from app.schemas.estoque import EstoqueCreate, EstoqueResponse
from datetime import datetime

router = APIRouter(prefix="/estoque", tags=["estoque"])


@router.post("/", response_model=EstoqueResponse)
def criar_item(EstoqueSchema: EstoqueCreate, db: Session = Depends(get_db)):
    novo = Estoque(
        nome_item=EstoqueSchema.nome_item,
        quantidade=EstoqueSchema.quantidade,
        custo_unitario=EstoqueSchema.custo_unitario,
        preco_venda=EstoqueSchema.preco_venda,
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
        raise HTTPException(
            status_code=400, detail=f"Erro ao criar item do estoque: {str(e)}"
        )


@router.get("/", response_model=list[EstoqueResponse])
def listar_itens(db: Session = Depends(get_db)):
    return db.query(Estoque).all()


@router.get("/{estoque_id}", response_model=EstoqueResponse)
def obter_item(estoque_id: int, db: Session = Depends(get_db)):
    estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Item do estoque não encontrado")
    return estoque


@router.delete("/{estoque_id}", response_model=dict)
def deletar_item(estoque_id: int, db: Session = Depends(get_db)):
    estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Item do estoque não encontrado")
    else:
        db.delete(estoque)
        db.commit()
        return {"detail": "Item do estoque deletado com sucesso"}


@router.put("/{estoque_id}", response_model=EstoqueResponse)
def atualizar_item(
    estoque_id: int, EstoqueSchema: EstoqueCreate, db: Session = Depends(get_db)
):
    estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Item do estoque não encontrado")
    else:
        estoque.nome_item = EstoqueSchema.nome_item
        estoque.quantidade = EstoqueSchema.quantidade
        estoque.custo_unitario = EstoqueSchema.custo_unitario
        estoque.preco_venda = EstoqueSchema.preco_venda
        estoque.ativo = EstoqueSchema.ativo
        estoque.passive = EstoqueSchema.passive
        estoque.marca = EstoqueSchema.marca
        estoque.descricao = EstoqueSchema.descricao
        estoque.unidade_medida = EstoqueSchema.unidade_medida

        try:
            db.commit()
            db.refresh(estoque)
            return estoque
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=400, detail=f"Erro ao atualizar item do estoque: {str(e)}"
            )
    return estoque
