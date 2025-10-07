from fastapi import FastAPI
from app.api import routes_vendas, user
from app.core.database import Base, engine

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Aqui está o objeto que o Uvicorn procura
app = FastAPI(title="API de Agendamento")

# Rotas
app.include_router(routes_vendas.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"mensagem": "Backend de Agendamento ativo!"}
