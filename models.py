# Importa tipos de ddos do SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
# Importa a base do banco de dados
from database import Base

# Define o modelo de tarefa
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)