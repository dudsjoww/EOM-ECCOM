from app.core.database import Base, engine

print("⚠️ Resetando banco de dados...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("✅ Banco recriado com sucesso!")
