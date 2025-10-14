from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tatuador import Tatuador
from app.models.pedidos import Pedido
from app.schemas.pedidos import PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResponse)
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo = Pedido(
        cliente_id=pedido.cliente_id,
        tatuador_id=pedido.tatuador_id,
        area_corpo=pedido.area_corpo,
        tamanho=pedido.tamanho,
        imagem_png=pedido.imagem_png,
        coordenadas=pedido.coordenadas,
        status="solicitado"
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()
