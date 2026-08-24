from typing import Optional

from pydantic import BaseModel


class ServicoSchema(BaseModel):
    id: Optional[int]
    nome_servico: str
    preco: float
    duracao_minutos: int

    class Config:
        orm_mode = True