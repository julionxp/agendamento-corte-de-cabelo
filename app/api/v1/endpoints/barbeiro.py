from typing import List

from fastapi import APIRouter, Response, HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.barbeiro_model import BarbeiroModel
from schemas.barbeiro_schema import BarbeiroSchema, BarbeiroUpdateSchema

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


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BarbeiroSchema)
async def post_barbeiro(barbeiro: BarbeiroSchema, db: AsyncSession = Depends(get_session)):
    novo_barbeiro = BarbeiroModel(
        nome=barbeiro.nome,
        email=barbeiro.email,
        telefone=barbeiro.telefone,
    )

    db.add(novo_barbeiro)
    await db.commit()

    return novo_barbeiro


@router.put('/{barbeiro_id}', status_code=status.HTTP_200_OK, response_model=BarbeiroUpdateSchema)
async def put_barbeiro(barbeiro_id: int, barbeiro: BarbeiroUpdateSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BarbeiroModel).filter(BarbeiroModel.id == barbeiro_id)
        result = await session.execute(query)
        barbeiro_up = result.scalar_one_or_none()

        if not barbeiro_up:
            raise HTTPException(detail='Barbeiro não encontrado', status_code=status.HTTP_404_NOT_FOUND)

        if barbeiro_up:
            if barbeiro.nome is not None:
                barbeiro_up.nome = barbeiro.nome
            if barbeiro.email is not None:
                barbeiro_up.email = barbeiro.email
            if barbeiro.telefone is not None:
                barbeiro_up.telefone = barbeiro.telefone

            await session.commit()

            return barbeiro_up           


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
