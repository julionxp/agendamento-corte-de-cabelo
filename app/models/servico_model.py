from core.configs import settings

from sqlalchemy import Column, Integer, String, DECIMAL

from decimal import Decimal


class ServicoModel(settings.DBBaseModel):
    __tablename__ = 'servicos'
 
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome_servico: str = Column(String(100), nullable=False)
    preco: Decimal = Column(DECIMAL, nullable=False)
    duracao_minutos: int = Column(Integer, nullable=False)