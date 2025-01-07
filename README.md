# To-Do List API

This project is a task management API, developed as part of a technical challenge. The API was built using **FastAPI** and has CRUD functionality to manage tasks, as well as JWT authentication.

## Main Features
- Create a new task.
- List all tasks.
- Update an existing task.
- Delete a task.
- View a specific task by ID.

## Technologies Used
- **Python 3.10**
- **FastAPI**: Framework for building RESTful APIs.
- **SQLModel**: ORM for database integration.
- **SQLite**: Relational database.
- **Uvicorn**: ASGI server to run the application.
- **Python-dotenv**: Environment variable management.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SEU_USUARIO/Desafio_Tecnico-Api_Gerenciamento.git
2. Navigate to the project directory:
   ```bash
   cd Desafio_Tecnico-Api_Gerenciamento
3. Create a virtual environment:
   ```bash
   python -m venv venv
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
6. Create a `.env` file in the root directory and add the following environment variables:
   ```
   DATABASE_URL=sqlite:///./database.db
   JWT_SECRET_KEY=your_secret_key
   JWT_ALGORITHM=HS256
7. Start the development server:
   ```bash
   uvicorn main:app --reload

## Usage
Once the server is running, you can access the API documentation at `http://localhost:8000/docs`. The documentation provides information about the available endpoints, request/response schemas, and authentication requirements.

## API
The API provides the following endpoints:

- `POST /tasks`: Create a new task.
- `GET /tasks`: List all tasks.
- `GET /tasks/{task_id}`: Retrieve a specific task by ID.
- `PUT /tasks/{task_id}`: Update an existing task.
- `DELETE /tasks/{task_id}`: Delete a task.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Testing
To run the tests, execute the following command:
```bash
pytest tests/
```
