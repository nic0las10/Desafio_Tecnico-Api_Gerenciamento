from fastapi import FastAPI, HTTPException, Depends, status, Query
from sqlmodel import Session, select
from app.database import engine, init_db
from app.models import Tarefa, TarefaBase
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import criar_token_acesso, verificar_senha, gerar_hash_senha
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
import requests
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

# URL da API pública
URL = "https://jsonplaceholder.typicode.com/todos"

# Função lifespan substituindo o método @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Inicializar o banco de dados
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")  # Configuração do cache
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

# Endpoint para listar todas as tarefas com filtros e paginação (Protegido)
@app.get("/tarefas", response_model=list[Tarefa])
@cache(expire=60)  # Cache configurado para expirar em 60 segundos
def listar_tarefas(
    estado: Optional[str] = Query(
        None,
        pattern="^(pendente|em andamento|concluída)$",  # Substituí regex por pattern
        description="Filtrar tarefas pelo estado ('pendente', 'em andamento', 'concluída')"
    ),
    skip: int = Query(0, ge=0, description="Número de tarefas a pular para paginação"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de tarefas a retornar (máximo: 100)"),
    token: str = Depends(oauth2_scheme)
):
    """Lista tarefas com suporte a filtros por estado e paginação."""
    with Session(engine) as session:
        # Base da consulta
        query = select(Tarefa)

        # Aplicar filtro por estado, se fornecido
        if estado:
            query = query.where(Tarefa.estado == estado)

        # Adicionar paginação
        tarefas = session.exec(query.offset(skip).limit(limit)).all()
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
@cache(expire=30)  # Cache configurado para expirar em 30 segundos
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

def buscar_tarefas_externas():
    # Fazendo a requisição para a API
    response = requests.get(URL)
    
    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        tarefas = response.json()  # Converte o JSON recebido em uma lista de dicionários
        
        with Session(engine) as session:  # Conexão com o banco de dados
            for tarefa in tarefas:
                # Verifica se a tarefa já existe no banco pelo título
                tarefa_existente = session.query(Tarefa).filter(Tarefa.titulo == tarefa["title"]).first()
                
                if not tarefa_existente:  # Se a tarefa não existir, cria uma nova
                    nova_tarefa = Tarefa(
                        titulo=tarefa["title"],
                        descricao="Tarefa importada da API JSON Placeholder",
                        estado="pendente" if not tarefa["completed"] else "concluída"
                    )
                    session.add(nova_tarefa)  # Adiciona a tarefa à sessão
            
            session.commit()  # Salva todas as mudanças no banco
        print("Tarefas externas adicionadas com sucesso.")
    else:
        print(f"Erro ao buscar tarefas: {response.status_code}")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas"}

if __name__ == "__main__":
    buscar_tarefas_externas()

