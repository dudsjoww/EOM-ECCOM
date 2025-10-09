from app.core.database import Base, engine
from app.models.user import User
from app.models.pedidos import Pedido
from app.models.tatuador import Tatuador
from app.models.horario_de_trabalho import HorariosdeTrabalho

print("🛠 Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")