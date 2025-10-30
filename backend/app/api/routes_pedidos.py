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
        status="solicitado",
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.delete("/{pedido_id}", response_model=dict)
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    else:
        db.delete(pedido)
        db.commit()
        return {"detail": "Pedido deletado com sucesso"}


@router.put("/{pedido_id}", response_model=PedidoResponse)
def atualizar_pedido(
    pedido_id: int, pedido: PedidoCreate, db: Session = Depends(get_db)
):
    pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    else:
        pedido_db.cliente_id = pedido.cliente_id
        pedido_db.tatuador_id = pedido.tatuador_id
        pedido_db.area_corpo = pedido.area_corpo
        pedido_db.tamanho = pedido.tamanho
        pedido_db.imagem_png = pedido.imagem_png
        pedido_db.coordenadas = pedido.coordenadas
        db.commit()
        db.refresh(pedido_db)
        return pedido_db


@router.put("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status_pedido(pedido_id: int, status: str, db: Session = Depends(get_db)):
    pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    else:
        pedido_db.status = status
        db.commit()
        db.refresh(pedido_db)
        return pedido_db
