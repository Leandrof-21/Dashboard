from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão padrão com o Postgres que subi no Docker
DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/dashboard_db"

# Motor da conexãodo SQLAlchemy
engine = create_engine(DATABASE_URL)

# Fábrica de sessões para requisições
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos de tabelas
Base = declarative_base()

# Função que vai auxiliar para injetar a sessão do banco nas rotas API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()