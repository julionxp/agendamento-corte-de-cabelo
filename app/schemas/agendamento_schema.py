from typing import Optional

from pydantic import BaseModel, ConfigDict

from datetime import datetime


class AgendamentoSchema(BaseModel):
    data_hora_inicio: datetime

    usuario_id: int
    barbeiro_id: int
    servico_id: int


class AgendamentoSchemaBase(BaseModel):
    id: Optional[int] = None
    data_hora_inicio: datetime

    usuario_id: int
    barbeiro_id: int
    servico_id: int

    model_config = ConfigDict(from_attributes=True)


class AgendamentoUpdateSchema(BaseModel):
    data_hora_inicio: Optional[datetime] = None
    confirmado: Optional[bool] = None

    barbeiro_id: Optional[int] = None
    servico_id: Optional[int] = None