from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.venda_consumivel import Venda_Consumivel
from app.schemas.venda_consumivel import VendaConsumivelCreate, VendaConsumivelResponse

router = APIRouter(prefix="/vendaconsumivel", tags=["VendaConsumivel"])


@router.post("/", response_model=VendaConsumivelResponse)
def criar_pedido(Schema: VendaConsumivelCreate, db: Session = Depends(get_db)):
    novo = Venda_Consumivel(
        item_id=Schema.item_id,
        quantidade=Schema.quantidade,
        preco_final=Schema.preco_final,
        pedidos_id=Schema.pedidos_id,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[VendaConsumivelResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Venda_Consumivel).all()
