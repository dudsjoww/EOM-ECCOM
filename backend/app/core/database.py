from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Cria engine com PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base dos modelos ORM
Base = declarative_base()

# Dependency para endpoints FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Teste de conexão (temporário)
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        if result.scalar() == 1:
            print("✅ Conexão com o banco OK!")
        else:
            print("❌ Conexão falhou!")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
