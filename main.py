# main.py
"""
FastAPI Todo API

API para gerenciamento de tarefas usando FastAPI e SQLAlchemy.
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
# Cria as tabelas do banco de dados
models.Base.metadata.create_all(bind=engine)
# Cria a instância do FastAPI
app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db(): 
    """
    Docstring para a função get_db, que é uma dependência do FastAPI para obter a sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar uma nova tarefa
@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    a função create_task recebe um objeto TaskCreate, que é um modelo Pydantic para a criação de tarefas, e a sessão do banco de dados como dependência.
    Ela cria uma nova instância do modelo Task com os dados fornecidos, adiciona a nova tarefa ao banco de dados, confirma a transação e retorna a tarefa criada.
    """
    new_task = models.Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# Rota para listar todas as tarefas
@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


# ----------------------------
# Atualizar uma tarefa existente
# ----------------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, db: Session = Depends(get_db)):
    """
    A função update_task recebe o id da tarefa a ser atualizada e a sessão do banco de dados como dependência. 
    Ela consulta o banco de dados para encontrar a tarefa com o id fornecido. 
    Se a tarefa for encontrada, o status de conclusão da tarefa é alternado (de True para False ou vice-versa) e a transação é confirmada. 
    A função retorna uma mensagem indicando se a tarefa foi atualizada com sucesso ou se a tarefa não foi encontrada.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task :
        task.completed = not task.completed
        db.commit()
        return {"message": "Task updated successfully"}
    
    return {"message": "Task not found"}

#-----------------------------
# Deletar uma tarefa
#-----------------------------

@app.delete("/tasks/{task_id}") # Rota para deletar uma tarefa, recebe o id da tarefa a ser deletada e a sessão do banco de dados como dependência
def delete_task(task_id: int, db: Session = Depends(get_db)): # task_id é o id da tarefa a ser deletada, db é a sessão do banco de dados
 
    """  A função delete_task recebe o id da tarefa a ser deletada e a sessão do banco de dados como dependência. 
    Ela consulta o banco de dados para encontrar a tarefa com o id fornecido. 
    Se a tarefa for encontrada, ela é deletada do banco de dados e a transação é confirmada. 
    A função retorna uma mensagem indicando se a tarefa foi deletada com sucesso ou se a tarefa não foi encontrada."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    
    return {"message": "Task not found"}