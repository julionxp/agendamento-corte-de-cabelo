from fastapi import APIRouter

from api.v1.endpoints import usuario
from api.v1.endpoints import barbeiro
from api.v1.endpoints import servico


api_router = APIRouter()
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(barbeiro.router, prefix='/barbeiros', tags=['barbeiros'])
api_router.include_router(servico.router, prefix='/servicos', tags=['servicos'])