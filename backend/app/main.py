from fastapi import FastAPI
from app.api import (
    routes_usuarios,
    routes_tatuadores,
    routes_pedidos,
    routes_horarios,
    routes_todos_os_horarios,
    routes_estoque,
    routes_agendamentos,
    routes_venda_consumivel,
    routes_orcamentos,
    routes_sessao,
    routes_refresh_token,
)

from app.middleware.auth_middleware import AuthMiddleware


app = FastAPI(title="Soyve Tattoo API")

app.add_middleware(AuthMiddleware)

app.include_router(routes_usuarios.router)
app.include_router(routes_tatuadores.router)
app.include_router(routes_horarios.router)
app.include_router(routes_todos_os_horarios.router)
app.include_router(routes_estoque.router)
app.include_router(routes_agendamentos.router)
app.include_router(routes_venda_consumivel.router)
app.include_router(routes_pedidos.router)
app.include_router(routes_orcamentos.router)
app.include_router(routes_sessao.router)
app.include_router(routes_refresh_token.router)
