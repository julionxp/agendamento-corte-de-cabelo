from typing import List

from fastapi import APIRouter, Response, HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.barbeiro_model import BarbeiroModel
from schemas.barbeiro_schema import BarbeiroSchema

from core.deps import get_session


router = APIRouter()



@router.get('/{barbeiro_id}', status_code=status.HTTP_200_OK, response_model=BarbeiroSchema)
async def get_barbeiro(barbeiro_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BarbeiroModel).filter(BarbeiroModel.id == barbeiro_id)
        result = await session.execute(query)
        barbeiro = result.scalar_one_or_none()

        if barbeiro:
            return barbeiro
        else:
            raise HTTPException(detail='Barbeiro não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[BarbeiroSchema])
async def get_barbeiros(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BarbeiroModel)
        result = await session.execute(query)
        barbeiros: List[BarbeiroModel] = result.scalars().unique().all()

        return barbeiros


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[BarbeiroSchema])
async def post_barbeiros(barbeiros: List[BarbeiroSchema], db: AsyncSession = Depends(get_session)):
    novos_barbeiros = [
        BarbeiroModel(
            nome=barbeiro.nome,
            email=barbeiro.email,
            telefone=barbeiro.telefone,
        )
        for barbeiro in barbeiros
    ]

    db.add_all(novos_barbeiros)
    await db.commit()

    return novos_barbeiros


@router.put('/{barbeiro_id}', status_code=status.HTTP_200_OK, response_model=BarbeiroSchema)
async def put_barbeiro(barbeiro_id: int, barbeiro: BarbeiroSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BarbeiroModel).filter(BarbeiroModel.id == barbeiro_id)
        result = await session.execute(query)
        barbeiro_up = result.scalar_one_or_none()

        if barbeiro_up:
            barbeiro_up.nome = barbeiro.nome
            barbeiro_up.email = barbeiro.email
            barbeiro_up.telefone = barbeiro.telefone

            await session.commit()

            return barbeiro_up

        else:
            raise HTTPException(detail='Barbeiro não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{barbeiro_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_barbeiro(barbeiro_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BarbeiroModel).filter(BarbeiroModel.id == barbeiro_id)
        result = await session.execute(query)
        barbeiro_del = result.scalar_one_or_none()

        if barbeiro_del:
            await session.delete(barbeiro_del)
            await session.commit()
            
            return Response('Barbeiro apagado com sucesso!')

        else:
            raise HTTPException(detail='Barbeiro não encontrado', status_code=status.HTTP_404_NOT_FOUND)
