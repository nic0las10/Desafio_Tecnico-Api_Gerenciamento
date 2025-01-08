from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import Session, select
from app.database import engine, init_db
from app.models import Tarefa, TarefaBase
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import criar_token_acesso, verificar_senha, gerar_hash_senha
from contextlib import asynccontextmanager
from datetime import datetime


# Função lifespan substituindo o método @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Inicializar o banco de dados
    yield  # Aqui pode ser usado para finalizar recursos, se necessário

# Inicializando a aplicação com o lifespan
app = FastAPI(lifespan=lifespan)

# Simulação de um "banco de dados" para usuários
fake_users_db = {
    "usuario1": {
        "username": "usuario1",
        "full_name": "Usuario Um",
        "email": "usuario1@example.com",
        "hashed_password": gerar_hash_senha("senha123"),
        "disabled": False,
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def autenticar_usuario(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verificar_senha(password, user["hashed_password"]):
        return None
    return user




# Endpoint de login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_token_acesso({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# Endpoint para listar todas as tarefas (Protegido)
@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas(token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        tarefas = session.exec(select(Tarefa)).all()
        return tarefas

# Endpoint para criar uma nova tarefa (Protegido)
@app.post("/tarefas", response_model=Tarefa, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: TarefaBase, token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        nova_tarefa = Tarefa(
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            estado=tarefa.estado,
            data_criacao=tarefa.data_criacao or datetime.utcnow(),
            data_atualizacao=tarefa.data_atualizacao or datetime.utcnow()
        )
        session.add(nova_tarefa)
        session.commit()
        session.refresh(nova_tarefa)
        return nova_tarefa

# Endpoint para obter uma tarefa pelo ID (Protegido)
@app.get("/tarefas/{id}", response_model=Tarefa)
def obter_tarefa(id: int, token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        tarefa = session.get(Tarefa, id)
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return tarefa

# Endpoint para atualizar uma tarefa existente (Protegido)
@app.put("/tarefas/{id}", response_model=Tarefa)
def atualizar_tarefa(id: int, tarefa_atualizada: TarefaBase, token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        tarefa = session.get(Tarefa, id)
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        
        tarefa.titulo = tarefa_atualizada.titulo
        tarefa.descricao = tarefa_atualizada.descricao
        tarefa.estado = tarefa_atualizada.estado
        tarefa.data_atualizacao = tarefa_atualizada.data_atualizacao or datetime.utcnow()

        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa

# Endpoint para deletar uma tarefa existente (Protegido)
@app.delete("/tarefas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(id: int, token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        tarefa = session.get(Tarefa, id)
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        session.delete(tarefa)
        session.commit()
        return

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas"}
