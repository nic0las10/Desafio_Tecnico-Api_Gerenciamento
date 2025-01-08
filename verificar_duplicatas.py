from sqlmodel import Session, select, func
from app.database import engine
from app.models import Tarefa

with Session(engine) as session:
    duplicatas = session.exec(
        select(Tarefa.titulo, func.count(Tarefa.id))
        .group_by(Tarefa.titulo)
        .having(func.count(Tarefa.id) > 1)
    ).all()

    if duplicatas:
        print("Tarefas Duplicadas Encontradas:")
        for titulo, count in duplicatas:
            print(f"Título: {titulo} - Quantidade: {count}")
    else:
        print("Nenhuma duplicata encontrada!")
