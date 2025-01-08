from sqlmodel import Session, select
from app.database import engine
from app.models import Tarefa

with Session(engine) as session:
    tarefas = session.exec(select(Tarefa)).all()
    for tarefa in tarefas:
        print(tarefa.titulo, tarefa.estado)
