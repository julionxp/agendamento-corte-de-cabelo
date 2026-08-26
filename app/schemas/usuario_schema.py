from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: EmailStr
    telefone: str

    model_config = ConfigDict(from_attributes=True)


class UsuarioUpdateSchema(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None