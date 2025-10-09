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
        ativo=usuario.ativo
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user

@router.get("/", response_model=list[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()
