from typing import List

from fastapi import APIRouter, Response, HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.servico_model import ServicoModel
from schemas.servico_schema import ServicoSchema

from core.deps import get_session


router = APIRouter()


@router.get('/{servico_id}', status_code=status.HTTP_200_OK, response_model=ServicoSchema)
async def get_servico(servico_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == servico_id)
        result = await session.execute(query)
        servico = result.scalar_one_or_none()

        if servico:
            return servico
        else:
            raise HTTPException(detail='Serviço não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ServicoSchema])
async def get_servicos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel)
        result = await session.execute(query)
        servicos: List[ServicoModel] = result.scalars().unique().all()

        return servicos


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[ServicoSchema])
async def post_servicos(servicos: List[ServicoSchema], db: AsyncSession = Depends(get_session)):
    novos_servicos = [
        ServicoModel(
            nome_servico=servico.nome_servico,
            preco=servico.preco,
            duracao_minutos=servico.duracao_minutos,
        )
        for servico in servicos
    ]

    db.add_all(novos_servicos)
    await db.commit()

    return novos_servicos


@router.put('/{servico_id}', status_code=status.HTTP_200_OK, response_model=ServicoSchema)
async def put_servico(servico_id: int, servico: ServicoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == servico_id)
        result = await session.execute(query)
        servico_up = result.scalar_one_or_none()

        if servico_up:
            servico_up.nome_servico = servico.nome_servico
            servico_up.preco = servico.preco
            servico_up.duracao_minutos = servico.duracao_minutos

            await session.commit()

            return servico_up

        else:
            raise HTTPException(detail='Serviço não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{servico_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_servico(servico_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == servico_id)
        result = await session.execute(query)
        servico_del = result.scalar_one_or_none()

        if servico_del:
            await session.delete(servico_del)
            await session.commit()
            
            return Response('Serviço apagado com sucesso!')

        else:
            raise HTTPException(detail='Serviço não encontrado', status_code=status.HTTP_404_NOT_FOUND)
