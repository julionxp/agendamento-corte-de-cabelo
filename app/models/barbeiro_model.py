from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey


class BarbeiroModel(settings.DBBaseModel):
    __tablename__ = 'barbeiros'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False)
    telefone: str = Column(String(20), nullable=False)