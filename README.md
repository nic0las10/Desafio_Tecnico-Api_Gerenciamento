# **API de Gerenciamento de Tarefas**

Uma API robusta e escalável para gerenciamento de tarefas (To-Do List), desenvolvida com **FastAPI**. O projeto segue boas práticas de desenvolvimento, como autenticação JWT, validação de dados com Pydantic, documentação automática e testes unitários com Pytest.

## **Objetivo**
Fornecer uma API que permita o gerenciamento de tarefas de maneira eficiente e segura, atendendo às seguintes funcionalidades:
- Criar, listar, atualizar e excluir tarefas.
- Visualizar uma tarefa específica pelo ID.
- Autenticação com JWT para proteger os endpoints.

---

## **Funcionalidades**

### **Endpoints Principais**
| Método | Endpoint         | Descrição                          |
|--------|------------------|------------------------------------|
| POST   | `/login`         | Autenticação e geração de token JWT. |
| POST   | `/tarefas`       | Criar uma nova tarefa.             |
| GET    | `/tarefas`       | Listar todas as tarefas.           |
| GET    | `/tarefas/{id}`  | Obter uma tarefa pelo ID.          |
| PUT    | `/tarefas/{id}`  | Atualizar uma tarefa existente.    |
| DELETE | `/tarefas/{id}`  | Excluir uma tarefa.                |

### **Modelo de Tarefa**
Cada tarefa contém os seguintes campos:
- **id**: Identificador único (inteiro, autoincrementado).
- **titulo**: Título da tarefa (string, obrigatório).
- **descricao**: Descrição da tarefa (string, opcional).
- **estado**: Estado da tarefa (string, obrigatório: "pendente", "em andamento", "concluída").
- **data_criacao**: Data de criação (gerada automaticamente).
- **data_atualizacao**: Data da última atualização (gerada automaticamente).

---

## **Tecnologias Utilizadas**
- **Python 3.10**: Linguagem de programação.
- **FastAPI**: Framework para construção de APIs RESTful.
- **SQLModel**: ORM para integração com o banco de dados.
- **SQLite**: Banco de dados leve e eficiente.
- **Alembic**: Gerenciamento de migrações de banco de dados.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **Pytest**: Framework para testes unitários.
- **JWT**: Autenticação segura.
- **FastAPI-Cache**: Implementação de caching nos endpoints.
- **Docker**: Ferramenta de containerização para facilitar o desenvolvimento.
- **JSON Placeholder**: API pública usada para importar tarefas no crawler.

---

## **Instalação e Configuração**

### **Pré-requisitos**
- Python 3.10 ou superior.
- Gerenciador de pacotes `pip`.
- Docker (opcional).

### **Passos para Configuração**
1. Clone o repositório:
   ```bash
   git clone https://github.com/nic0las10/Desafio_Tecnico-Api_Gerenciamento.git
   cd Desafio_Tecnico-Api_Gerenciamento
2. Crie e ative o ambiente virtual:
    ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
4. Crie o arquivo .env no diretório raiz e adicione as variáveis de ambiente:
    ```env
   DATABASE_URL=sqlite:///./database.db
   SECRET_KEY=(chave no .env.exemple )
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Inicialize o banco de dados:
   ```bash
   python -m app.database
6. Inicie o servidor:
    ```bash
    uvicorn app.main:app --reload
### **Acesse a documentação interativa:**

-Swagger: http://127.0.0.1:8000/docs
-Redoc: http://127.0.0.1:8000/redoc

---

### **Testes Unitários**

1. ### **Execute os testes unitários:**
   ```bash
   pytest tests/
   
2. **O que os testes cobrem:**
- CRUD das tarefas (criação, leitura, atualização, exclusão).
- Autenticação JWT.

---

### **Dockerização**

1. ### **Construa a imagem Docker:**
   ```bash
   docker build -t desafio_tecnico:latest .
   
2. **Execute o container:**
   ```bash
   docker run -d -p 8001:8000 desafio_tecnico:latest

3-   Acesse a API em: http://127.0.0.1:8001.

   
### **Extras Implementados**
Filtros e Paginação:
- Filtros: Permite listar tarefas pelo estado (pendente, em andamento, concluída)..
- Paginação: Utilize os parâmetros skip e limit para navegar entre os resultados.

 **Crawler**
- Importa tarefas automaticamente da API pública JSON Placeholder.
- As tarefas importadas são verificadas para evitar duplicatas.


### **Caching**
O caching foi implementado nos endpoints de leitura para otimizar o desempenho e reduzir o tempo de resposta das requisições. 

#### **Configuração**
- **Cache no endpoint `/tarefas/{id}`**:
  - Expira em 30 segundos.
  - Armazena o resultado da requisição para uma tarefa específica pelo ID.
- **Cache no endpoint `/tarefas`**:
  - Expira em 60 segundos.
  - Armazena a lista de tarefas, incluindo possíveis filtros e paginação.

---

## **Referências**

- [FastAPI](https://fastapi.tiangolo.com/) - Framework utilizado para a construção de APIs rápidas e modernas.
- [SQLModel](https://sqlmodel.tiangolo.com/) - ORM utilizado para gerenciar o banco de dados relacional de maneira eficiente.
- [Alembic](https://alembic.sqlalchemy.org/) - Ferramenta para gerenciamento de migrações de banco de dados.
- [Pytest](https://pytest.org/) - Framework para a criação de testes unitários abrangentes.
- [JSON Placeholder](https://jsonplaceholder.typicode.com/) - API pública utilizada no crawler para importar dados fictícios de tarefas.
- [FastAPI-Cache](https://fastapi-cache.tiangolo.com/) - Biblioteca para implementação de caching nos endpoints da API.

  
---

## **Licença**
 Este projeto está licenciado sob a licença [MIT](LICENSE). Consulte o arquivo `LICENSE` para obter mais detalhes.









    
   
