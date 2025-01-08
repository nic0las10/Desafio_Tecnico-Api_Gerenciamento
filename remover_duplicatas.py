from sqlmodel import Session, select, func
from app.database import engine
from app.models import Tarefa

with Session(engine) as session:
    # Identificar títulos duplicados
    duplicatas = session.exec(
        select(Tarefa.titulo, func.count(Tarefa.id))
        .group_by(Tarefa.titulo)
        .having(func.count(Tarefa.id) > 1)
    ).all()

    if duplicatas:
        print("Removendo tarefas duplicadas...")
        for titulo, count in duplicatas:
            # Buscar todas as tarefas com o título duplicado
            tarefas = session.exec(
                select(Tarefa).where(Tarefa.titulo == titulo)
            ).all()

            # Mantém a primeira ocorrência e remove as outras
            for tarefa in tarefas[1:]:
                session.delete(tarefa)

        session.commit()
        print("Duplicatas removidas com sucesso!")
    else:
        print("Nenhuma duplicata encontrada!")
