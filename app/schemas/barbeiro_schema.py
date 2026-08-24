from typing import Optional

from pydantic import BaseModel, ConfigDict


class BarbeiroSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    telefone: str

    model_config = ConfigDict(from_attributes=True)