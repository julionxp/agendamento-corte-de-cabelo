from typing import Optional

from pydantic import BaseModel, ConfigDict


class ServicoSchema(BaseModel):
    id: Optional[int] = None
    nome_servico: str
    preco: float
    duracao_minutos: int

    model_config = ConfigDict(from_attributes=True)