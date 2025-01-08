from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
from pydantic import ConfigDict  # Substitui a Config antiga


# Enum para os valores permitidos do campo "estado"
class EstadoTarefa(str, Enum):
    pendente = "pendente"
    em_andamento = "em andamento"
    concluida = "concluída"


# Base do modelo de tarefa
class TarefaBase(SQLModel):
    titulo: str
    descricao: Optional[str] = None  # Campo opcional
    estado: EstadoTarefa  # Usa o Enum para validar os valores permitidos
    data_criacao: datetime = Field(default_factory=datetime.utcnow)  # Adicionado valor padrão
    data_atualizacao: datetime = Field(default_factory=datetime.utcnow)  # Adicionado valor padrão


# Modelo completo da tabela de tarefas
class Tarefa(TarefaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Configuração para evitar redefinições da tabela
    model_config = ConfigDict(table_args={"extend_existing": True})
