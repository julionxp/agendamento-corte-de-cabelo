from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False)
    telefone: str = Column(String(20), nullable=False)
    
    # senha