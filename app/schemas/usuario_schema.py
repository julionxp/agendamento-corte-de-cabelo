from typing import Optional

from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    id: Optional[int]
    nome: str
    email: str
    telefone: str

    class Config:
        orm_mode = True