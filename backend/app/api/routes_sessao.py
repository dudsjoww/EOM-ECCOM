from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sessao import Sessao
from app.schemas.sessao import SessaoCreate, SessaoResponse

router = APIRouter(prefix="/sessao", tags=["Sessao"])


# TODO: Fazer validação do orçamento_id no create e update
# TODO: Verificar se o orçamento_id existe no banco

# =================================================================
# ==========         VALIDAÇÃO DE ERROS DAS VARIAVEIS       =======
# =================================================================

# TODO: Verificar se a duração da sessão bate com hora inicio e hora fim
# TODO: Fazer validação para não criar sessões em datas passadas
# TODO: Fazer validação para não criar sessões em horários fora do expediente
# TODO: Validar se o orçamento já está confirmado pelo cliente antes de criar a sessão


# TODO : Verificar se já existe sessão no mesmo horário com o mesmo tatuador (final)


@router.post("/", response_model=SessaoResponse)
def criar_sessao(SessaoSchema: SessaoCreate, db: Session = Depends(get_db)):
    novo = Sessao(
        orcamento_id=SessaoSchema.orcamento_id,
        duracao_horas=SessaoSchema.duracao_horas,
        data_sessao=SessaoSchema.data_sessao,
        hora_inicio=SessaoSchema.hora_inicio,
        hora_fim=SessaoSchema.hora_fim,
        observacao=SessaoSchema.observacao,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[SessaoResponse])
def listar_sessoes(db: Session = Depends(get_db)):
    return db.query(Sessao).all()


@router.get("/{sessao_id}", response_model=SessaoResponse)
def obter_sessao(sessao_id: int, db: Session = Depends(get_db)):
    sessao = db.query(Sessao).filter(Sessao.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessao não encontrada")
    return sessao


@router.delete("/{sessao_id}", response_model=dict)
def deletar_sessao(sessao_id: int, db: Session = Depends(get_db)):
    sessao = db.query(Sessao).filter(Sessao.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessao não encontrada")
    else:
        db.delete(sessao)
        db.commit()
        return {"detail": "Sessao deletada com sucesso"}


@router.put("/{sessao_id}", response_model=SessaoResponse)
def atualizar_sessao(
    sessao_id: int, SessaoSchema: SessaoCreate, db: Session = Depends(get_db)
):
    sessao = db.query(Sessao).filter(Sessao.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessao não encontrada")
    else:
        sessao.orcamento_id = SessaoSchema.orcamento_id
        sessao.data_sessao = SessaoSchema.data_sessao
        sessao.hora_inicio = SessaoSchema.hora_inicio
        sessao.hora_fim = SessaoSchema.hora_fim
        sessao.observacao = SessaoSchema.observacao

        db.commit()
        db.refresh(sessao)
    return sessao
