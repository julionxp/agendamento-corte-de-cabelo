from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class BarbeiroSchema(BaseModel):
    id: Optional[int]
    data_hora_inicio: datetime
    data_hora_fim: datetime
    confirmado: bool

    usuario_id: int
    barbeiro_id: int
    servico_id: int

    class Config:
        orm_mode = True