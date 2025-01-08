from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()


# Configurações básicas carregadas do .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



# Criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar a senha
def verificar_senha(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o hash da senha
def gerar_hash_senha(password):
    return pwd_context.hash(password)

# Função para criar o token JWT
def criar_token_acesso(dados: dict):
    to_encode = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiracao})
    token_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

# Função para validar o token JWT
def validar_token_acesso(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
