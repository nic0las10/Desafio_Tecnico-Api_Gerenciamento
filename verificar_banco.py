from sqlmodel import Session, select
from app.database import engine
from app.models import Tarefa

# Inicia uma sessão no banco de dados
with Session(engine) as session:
    # Executa um comando para listar todas as tarefas
    result = session.exec(select(Tarefa)).all()
    
    # Imprime o resultado
    print("Tarefas encontradas no banco de dados:")
    print(result)
