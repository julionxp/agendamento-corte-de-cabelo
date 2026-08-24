from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean


class AgendamentoModel(settings.DBBaseModel):
    __tablename__ = 'agendamentos'
 
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    confirmado: bool = Column(Boolean, nullable=False)

    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    barbeiro_id: int = Column(Integer, ForeignKey('barbeiros.id'))
    servico_id: int = Column(Integer, ForeignKey('servicos.id'))