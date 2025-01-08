from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from app.models import SQLModel  # Importa o SQLModel para usar o metadata
from app.database import engine  # Importa o engine do banco de dados configurado no projeto

# Este é o objeto de configuração do Alembic, que fornece
# acesso aos valores dentro do arquivo .ini em uso.
config = context.config

# Interpreta o arquivo de configuração para o Python logging.
# Esta linha configura os loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adiciona o metadata dos modelos para suporte ao 'autogenerate'
# Aqui definimos o target_metadata com o metadata do SQLModel
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Executa as migrações no modo 'offline'.

    Esta função configura o contexto com apenas uma URL,
    sem precisar de um Engine. Isso é útil quando o banco
    de dados não está disponível no ambiente local.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo 'online'.

    Neste cenário, criamos um Engine e associamos uma conexão ao contexto.
    """
    connectable = engine  # Usa o engine configurado no projeto

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detecta alterações nos tipos de colunas
        )

        with context.begin_transaction():
            context.run_migrations()


# Executa a função correta com base no modo de execução (offline ou online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
