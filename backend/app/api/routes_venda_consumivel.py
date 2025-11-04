from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.estoque import Estoque
from app.models.venda_consumivel import Venda_Consumivel
from app.schemas.venda_consumivel import VendaConsumivelCreate, VendaConsumivelResponse

router = APIRouter(prefix="/vendaconsumivel", tags=["VendaConsumivel"])

# TODO : Otimizar para uma função de validação reutilizável


@router.post("/", response_model=VendaConsumivelResponse)
def criar_pedido(Schema: VendaConsumivelCreate, db: Session = Depends(get_db)):
    if not Schema.quantidade or Schema.quantidade <= 0:
        raise HTTPException(
            status_code=400, detail="Quantidade deve ser maior que zero"
        )
    if not db.query(Estoque).filter(Estoque.id == Schema.item_id).first():
        raise HTTPException(status_code=404, detail="Item não encontrado no estoque")
    elif not Schema.preco_final or Schema.preco_final < 0:
        item = db.query(Estoque).filter(Estoque.id == Schema.item_id).first()
        Schema.preco_final = float(item.preco_venda)

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


@router.get("/{venda_id}", response_model=VendaConsumivelResponse)
def obter_pedido(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(Venda_Consumivel).filter(Venda_Consumivel.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


@router.delete("/{venda_id}", response_model=dict)
def deletar_pedido(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(Venda_Consumivel).filter(Venda_Consumivel.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    else:
        db.delete(venda)
        db.commit()
        return {"detail": "Venda deletada com sucesso"}


@router.put("/{venda_id}", response_model=VendaConsumivelResponse)
def atualizar_pedido(
    venda_id: int, Schema: VendaConsumivelCreate, db: Session = Depends(get_db)
):
    venda = db.query(Venda_Consumivel).filter(Venda_Consumivel.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    else:
        venda.item_id = Schema.item_id
        venda.quantidade = Schema.quantidade
        venda.preco_final = Schema.preco_final
        venda.pedidos_id = Schema.pedidos_id

        db.commit()
        db.refresh(venda)
    return venda
