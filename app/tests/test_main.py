from fastapi.testclient import TestClient
from app.main import app
from app.auth import criar_token_acesso
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


# Inicializa o cache para os testes
FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

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



# Teste para filtrar tarefas por estado
def test_filtrar_tarefas_por_estado():
    token = obter_token()
    # Cria tarefas com estados diferentes
    client.post(
        "/tarefas",
        json={"titulo": "Tarefa pendente", "descricao": "Descrição pendente", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    client.post(
        "/tarefas",
        json={"titulo": "Tarefa concluída", "descricao": "Descrição concluída", "estado": "concluída"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Filtra tarefas pendentes
    response = client.get(
        "/tarefas?estado=pendente",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    for tarefa in response.json():
        assert tarefa["estado"] == "pendente"



# Teste para verificar paginação
def test_paginacao_tarefas():
    token = obter_token()
    # Cria múltiplas tarefas
    for i in range(15):
        client.post(
            "/tarefas",
            json={"titulo": f"Tarefa {i+1}", "descricao": f"Descrição {i+1}", "estado": "pendente"},
            headers={"Authorization": f"Bearer {token}"}
        )

    # Lista tarefas com paginação
    response = client.get(
        "/tarefas?skip=5&limit=5",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 5  # Deve retornar exatamente 5 tarefas



# Teste para verificar acesso sem autenticação
def test_acesso_sem_autenticacao():
    response = client.get("/tarefas")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"





# Teste para criar tarefa com dados inválidos
def test_criar_tarefa_dados_invalidos():
    token = obter_token()
    # Tenta criar uma tarefa sem título (campo obrigatório)
    response = client.post(
        "/tarefas",
        json={"descricao": "Descrição sem título", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Unprocessable Entity





    # Teste para verificar caching no endpoint /tarefas/{id}
def test_cache_tarefa():
    token = obter_token()
    # Cria uma tarefa para testar o cache
    criar_response = client.post(
        "/tarefas",
        json={"titulo": "Cache Teste", "descricao": "Teste de cache", "estado": "pendente"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert criar_response.status_code == 201
    tarefa_id = criar_response.json()["id"]

    # Faz a primeira requisição (deve ir ao banco)
    primeira_response = client.get(
        f"/tarefas/{tarefa_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert primeira_response.status_code == 200

    # Faz a segunda requisição (deve usar o cache)
    segunda_response = client.get(
        f"/tarefas/{tarefa_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert segunda_response.status_code == 200

    # As respostas devem ser iguais
    assert primeira_response.json() == segunda_response.json()

