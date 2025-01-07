API de Gerenciamento de Tarefas
Este é um projeto de API para gerenciamento de tarefas (To-Do List) desenvolvido com FastAPI. Ele permite criar, listar, atualizar, visualizar e deletar tarefas. A API também conta com autenticação via JWT e validação de dados.

Configurações do Projeto
Requisitos
Python 3.10 ou superior
Git
SQLite (incluso no Python)
Instalação
Clone o repositório:

bash
Copiar código
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_DIRETORIO_DO_PROJETO>
Crie e ative um ambiente virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Inicialize o banco de dados:

bash
Copiar código
python -m app.database
Executando o Projeto
Execute o servidor:

bash
Copiar código
uvicorn app.main:app --reload
Acesse a documentação da API no navegador:

Swagger UI: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc
Endpoints da API
Autenticação
POST /login
Gera um token JWT para autenticação.
Body:

json
Copiar código
{
  "username": "usuario1",
  "password": "senha123"
}
Resposta:

json
Copiar código
{
  "access_token": "seu_token_jwt_aqui",
  "token_type": "bearer"
}
Gerenciamento de Tarefas
POST /tarefas
Cria uma nova tarefa.
Headers:
Authorization: Bearer <seu_token_jwt>
Body:

json
Copiar código
{
  "titulo": "Minha Tarefa",
  "descricao": "Detalhes da tarefa",
  "estado": "pendente"
}
GET /tarefas
Lista todas as tarefas.
Headers:
Authorization: Bearer <seu_token_jwt>

GET /tarefas/{id}
Visualiza uma tarefa específica pelo ID.
Headers:
Authorization: Bearer <seu_token_jwt>

PUT /tarefas/{id}
Atualiza uma tarefa existente.
Headers:
Authorization: Bearer <seu_token_jwt>
Body:

json
Copiar código
{
  "titulo": "Tarefa Atualizada",
  "descricao": "Detalhes atualizados",
  "estado": "em andamento"
}
DELETE /tarefas/{id}
Deleta uma tarefa existente.
Headers:
Authorization: Bearer <seu_token_jwt>

Executando Testes
Execute os testes unitários com Pytest:

bash
Copiar código
pytest
Certifique-se de que todos os testes passam.

Estrutura do Projeto
bash
Copiar código
Desafio_tecnico/
│
├── app/
│   ├── auth.py              # Lógica de autenticação e geração de JWT
│   ├── database.py          # Configuração e inicialização do banco de dados
│   ├── main.py              # Endpoints principais da API
│   ├── models.py            # Modelos SQLAlchemy e validações com Pydantic
│
├── tests/
│   ├── test_main.py         # Testes unitários para os endpoints
│
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação do projeto
Funcionalidades
Autenticação JWT para proteger os endpoints.
Validação de dados com Pydantic.
Suporte a operações CRUD para tarefas.
Documentação automática com Swagger.
Possíveis Melhorias
Implementar filtros e paginação na listagem de tarefas.
Dockerizar o projeto para facilitar a implantação.
Adicionar suporte para migrações com Alembic.
Implementar caching nos endpoints de leitura.
Desenvolvido por Nícolas de Macedo. 🚀
