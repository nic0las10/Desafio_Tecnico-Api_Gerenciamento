

# API de Lista de Tarefas

Este projeto é uma API de gerenciamento de tarefas, desenvolvida como parte de um desafio técnico. A API foi construída usando **FastAPI** e possui funcionalidade CRUD para gerenciar tarefas, além de autenticação JWT.

## Principais Funcionalidades
- Criar uma nova tarefa.
- Listar todas as tarefas.
- Atualizar uma tarefa existente.
- Excluir uma tarefa.
- Visualizar uma tarefa específica por ID.

## Tecnologias Utilizadas
- **Python 3.10**
- **FastAPI**: Framework para construção de APIs RESTful.
- **SQLModel**: ORM para integração com banco de dados.
- **SQLite**: Banco de dados relacional.
- **Uvicorn**: Servidor ASGI para executar a aplicação.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/Desafio_Tecnico-Api_Gerenciamento.git
2. Navegue até o diretório do projeto:
   ```bash
   cd Desafio_Tecnico-Api_Gerenciamento
3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
4. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No macOS/Linux: `source venv/bin/activate`
5. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
6. Crie um arquivo `.env` no diretório raiz e adicione as seguintes variáveis de ambiente:
   ```
   DATABASE_URL=sqlite:///./database.db
   JWT_SECRET_KEY=your_secret_key
   JWT_ALGORITHM=HS256
7. Inicie o servidor de desenvolvimento:
   ```bash
   uvicorn main:app --reload

## Uso
Uma vez que o servidor esteja em execução, você pode acessar a documentação da API em `http://localhost:8000/docs`. A documentação fornece informações sobre os endpoints disponíveis, esquemas de requisição/resposta e requisitos de autenticação.

## API
A API fornece os seguintes endpoints:

- `POST /tasks`: Criar uma nova tarefa.
- `GET /tasks`: Listar todas as tarefas.
- `GET /tasks/{task_id}`: Recuperar uma tarefa específica por ID.
- `PUT /tasks/{task_id}`: Atualizar uma tarefa existente.
- `DELETE /tasks/{task_id}`: Excluir uma tarefa.


## Testes
Para rodar os testes, execute o seguinte comando:
```bash
pytest tests/
```

Espero que isso ajude a preparar seu README para a entrevista. Se precisar de mais alguma coisa, estarei aqui para ajudar! Boa sorte na sua entrevista! 🍀
