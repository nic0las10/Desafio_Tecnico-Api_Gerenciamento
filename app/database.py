from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, create_engine

# Carregar o arquivo .env
load_dotenv()

# Recuperar variáveis do .env
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar o banco de dados
engine = create_engine(DATABASE_URL, echo=True)

# Função para inicializar o banco de dados
def init_db():
    SQLModel.metadata.create_all(engine)
