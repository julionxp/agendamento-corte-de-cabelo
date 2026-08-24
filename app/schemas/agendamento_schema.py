from typing import Optional

from pydantic import BaseModel, ConfigDict

from datetime import datetime


class BarbeiroSchema(BaseModel):
    id: Optional[int] = None
    data_hora_inicio: datetime
    data_hora_fim: datetime
    confirmado: bool

    usuario_id: int
    barbeiro_id: int
    servico_id: int

    model_config = ConfigDict(from_attributes=True)