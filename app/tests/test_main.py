from fastapi.testclient import TestClient
from app.main import app
from app.auth import criar_token_acesso

# Cria o cliente de testes
client = TestClient(app)

# Função para obter um token válido
def obter_token():
    response = client.post(
        "/login",
        data={"username": "usuario1", "password": "senha123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# Teste para criar uma nova tarefa
def test_criar_tarefa():
    token = obter_token()
    response = client.post(
        "/tarefas",
        json={"titulo": "Teste", "descricao": "Tarefa de teste", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["titulo"] == "Teste"

# Teste para listar todas as tarefas
def test_listar_tarefas():
    token = obter_token()
    # Cria duas tarefas para listar
    client.post(
        "/tarefas",
        json={"titulo": "Tarefa 1", "descricao": "Descrição 1", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    client.post(
        "/tarefas",
        json={"titulo": "Tarefa 2", "descricao": "Descrição 2", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Lista todas as tarefas
    response = client.get(
        "/tarefas",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 2  # Verifica se pelo menos 2 tarefas estão listadas

# Teste para obter uma tarefa pelo ID
def test_obter_tarefa():
    token = obter_token()
    # Cria uma tarefa para buscar
    criar_response = client.post(
        "/tarefas",
        json={"titulo": "Tarefa para buscar", "descricao": "Descrição de teste", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert criar_response.status_code == 201
    tarefa_id = criar_response.json()["id"]

    # Obtém a tarefa pelo ID
    response = client.get(
        f"/tarefas/{tarefa_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Tarefa para buscar"

# Teste para atualizar uma tarefa existente
def test_atualizar_tarefa():
    token = obter_token()
    # Cria uma tarefa para atualizar
    criar_response = client.post(
        "/tarefas",
        json={"titulo": "Descrição antiga", "descricao": "Antiga", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert criar_response.status_code == 201
    tarefa_id = criar_response.json()["id"]

    # Atualiza a tarefa criada
    response = client.put(
        f"/tarefas/{tarefa_id}",
        json={"titulo": "Atualizado", "descricao": "Descrição atualizada", "estado": "em andamento"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Atualizado"

# Teste para deletar uma tarefa existente
def test_deletar_tarefa():
    token = obter_token()
    # Cria uma tarefa para deletar
    criar_response = client.post(
        "/tarefas",
        json={"titulo": "Tarefa para deletar", "descricao": "Descrição qualquer", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert criar_response.status_code == 201
    tarefa_id = criar_response.json()["id"]

    # Deleta a tarefa criada
    response = client.delete(
        f"/tarefas/{tarefa_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # Tenta buscar a tarefa deletada
    buscar_response = client.get(
        f"/tarefas/{tarefa_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert buscar_response.status_code == 404
