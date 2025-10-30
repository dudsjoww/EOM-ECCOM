from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.orcamentos import Orcamentos
from app.schemas.orcamentos import OrcamentoCreate, OrcamentoResponse

router = APIRouter(prefix="/orcamentos", tags=["Orcamentos"])


@router.post("/", response_model=OrcamentoResponse)
def criar_orcamento(OrcamentoSchema: OrcamentoCreate, db: Session = Depends(get_db)):
    novo = Orcamentos(
        valor_sessao=OrcamentoSchema.valor_sessao,
        duracao_horas=OrcamentoSchema.duracao_horas,
        qtd_sessoes=OrcamentoSchema.qtd_sessoes,
        confirmado_cliente=OrcamentoSchema.confirmado_cliente,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[OrcamentoResponse])
def listar_orcamentos(db: Session = Depends(get_db)):
    return db.query(Orcamentos).all()


@router.get("/{orcamento_id}", response_model=OrcamentoResponse)
def obter_orcamento(orcamento_id: int, db: Session = Depends(get_db)):
    orcamento = db.query(Orcamentos).filter(Orcamentos.id == orcamento_id).first()
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return orcamento


@router.delete("/{orcamento_id}", response_model=dict)
def deletar_orcamento(orcamento_id: int, db: Session = Depends(get_db)):
    orcamento = db.query(Orcamentos).filter(Orcamentos.id == orcamento_id).first()
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    else:
        db.delete(orcamento)
        db.commit()
        return {"detail": "Orçamento deletado com sucesso"}


@router.put("/{orcamento_id}", response_model=OrcamentoResponse)
def atualizar_orcamento(
    orcamento_id: int, OrcamentoSchema: OrcamentoCreate, db: Session = Depends(get_db)
):
    orcamento = db.query(Orcamentos).filter(Orcamentos.id == orcamento_id).first()
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    else:
        orcamento.valor_sessao = OrcamentoSchema.valor_sessao
        orcamento.duracao_horas = OrcamentoSchema.duracao_horas
        orcamento.qtd_sessoes = OrcamentoSchema.qtd_sessoes
        orcamento.confirmado_cliente = OrcamentoSchema.confirmado_cliente
        db.commit()
        db.refresh(orcamento)
        return orcamento
