from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.estoque import Estoque
from app.models.venda_consumivel import Venda_Consumivel
from app.models.pedidos import Pedido
from app.schemas.venda_consumivel import VendaConsumivelCreate, VendaConsumivelResponse

router = APIRouter(prefix="/vendaconsumivel", tags=["VendaConsumivel"])

# TODO : Otimizar para uma função de validação reutilizável


@router.post("/", response_model=VendaConsumivelResponse)
def criar_pedido(Schema: VendaConsumivelCreate, db: Session = Depends(get_db)):
    if not Schema.quantidade or Schema.quantidade <= 0:
        raise HTTPException(
            status_code=400, detail="Quantidade deve ser maior que zero"
        )
    item = db.query(Estoque).filter(Estoque.id == Schema.item_id).first()
    pedido = db.query(Pedido).filter(Pedido.id == Schema.pedidos_id).first() is None
    outras_vendas = (
        db.query(Venda_Consumivel)
        .filter(
            Venda_Consumivel.item_id == Schema.item_id
            and Venda_Consumivel.pedidos_id == Schema.pedidos_id,
        )
        .first()
    )
    # raise HTTPException(
    #     status_code=400,
    #     detail=f"{outras_vendas is True}\n {outras_vendas.item_id} - {Schema.item_id}\n {outras_vendas.pedidos_id} - {Schema.pedidos_id}",
    # )

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no estoque")
    if Schema.preco_final is None or Schema.preco_final <= 0:
        if item.preco_venda is None:
            raise HTTPException(
                status_code=400,
                detail=f"O item '{item.nome_item}' não possui preço de venda definido.",
            )
        Schema.preco_final = round(item.preco_venda * Schema.quantidade, 2)
    if pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if outras_vendas:
        raise HTTPException(
            status_code=400,
            detail=f"Venda já registrada para este pedido e item, por favor apenas atualize ID:{outras_vendas.id} Item {item.nome_item}",
        )

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
