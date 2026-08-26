from typing import Optional

from pydantic import BaseModel, ConfigDict

from decimal import Decimal


class ServicoSchema(BaseModel):
    id: Optional[int] = None
    nome_servico: str
    preco: Decimal
    duracao_minutos: int

    model_config = ConfigDict(from_attributes=True)


class ServicoUpdateSchema(BaseModel):
    nome_servico: Optional[str] = None
    preco: Optional[Decimal] = None
    duracao_minutos: Optional[int] = None