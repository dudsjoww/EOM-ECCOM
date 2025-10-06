# app/api/routes_vendas.py
from fastapi import APIRouter

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.get("/")
def listar_vendas():
    return {"mensagem": "Listagem de vendas funcionando!"}
