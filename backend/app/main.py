from fastapi import FastAPI
from app.api import routes_usuarios, routes_tatuadores, routes_pedidos, routes_horarios, routes_todos_os_horarios
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soyve Tattoo API")

app.include_router(routes_usuarios.router)
app.include_router(routes_tatuadores.router)
app.include_router(routes_pedidos.router)
app.include_router(routes_horarios.router)
app.include_router(routes_todos_os_horarios.router)
