# importa a funcão create_engine do SQLAlchemy
from sqlalchemy import create_engine
# importa classe base para criar modelos ORM
from sqlalchemy.ext.declarative import declarative_base
# importa a classe Session para criar sessões de banco de dados
from sqlalchemy.orm import sessionmaker

# Define a URL de conexão com o banco de dados SQLite
DATABASE_URL = "sqlite:///./tasks.db"
# Cria o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()