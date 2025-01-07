from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from enum import Enum


# Enum para os valores permitidos do campo "estado"
class EstadoTarefa(str, Enum):
    pendente = "pendente"
    em_andamento = "em andamento"
    concluida = "concluída"


class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(max_length=255)  # Título obrigatório
    descricao: Optional[str] = None  # Descrição opcional
    estado: EstadoTarefa = Field(default=EstadoTarefa.pendente)  # Estado com valores limitados
    data_criacao: datetime = Field(default_factory=datetime.utcnow)  # Gerado automaticamente
    data_atualizacao: datetime = Field(default_factory=datetime.utcnow)  # Atualizado automaticamente
