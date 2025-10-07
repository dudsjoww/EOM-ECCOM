from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import user as crud_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.post("/")
def create_user(nome: str, email: str, senha: str, db: Session = Depends(get_db)):
    return crud_user.create_user(db, nome, email, senha)
