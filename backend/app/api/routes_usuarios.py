from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/", response_model=UserResponse)
def criar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_user = User(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=usuario.senha_hash,  # ideal: hashear depois
        ativo=usuario.ativo,
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user


@router.get("/", response_model=list[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def obter_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.delete("/{user_id}", response_model=dict)
def deletar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        db.delete(usuario)
        db.commit()
        return {"detail": "Usuário deletado com sucesso"}


@router.put("/{user_id}", response_model=UserResponse)
def atualizar_usuario(user_id: int, usuario: UserCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(User).filter(User.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        usuario_db.nome = usuario.nome
        usuario_db.email = usuario.email
        usuario_db.senha_hash = usuario.senha_hash  # ideal: hashear depois
        usuario_db.ativo = usuario.ativo
        db.commit()
        db.refresh(usuario_db)
        return usuario_db
