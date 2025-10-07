# create_db.py
from app.core.database import Base, engine
from app.models.user import User  # importa todos os modelos que quer criar

print("🛠 Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")