from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from app.database import engine
from app.models import Tarefa

app = FastAPI()

# Inicializar o banco de dados
@app.on_event("startup")
def on_startup():
    from app.database import init_db
    init_db()

# Endpoint para listar todas as tarefas
@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    with Session(engine) as session:
        tarefas = session.exec(select(Tarefa)).all()
        return tarefas

# Endpoint para criar uma nova tarefa
@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa):
    with Session(engine) as session:
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas"}
