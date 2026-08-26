from typing import List

from fastapi import APIRouter, Response, HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema, UsuarioUpdateSchema

from core.deps import get_session


router = APIRouter()



@router.get('/{usuario_id}', status_code=status.HTTP_200_OK, response_model=UsuarioSchema)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UsuarioSchema])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().unique().all()

        return usuarios


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema)
async def post_usuario(usuario: UsuarioSchema, db: AsyncSession = Depends(get_session)):
    novo_usuario = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email,
            telefone=usuario.telefone,
        )

    db.add(novo_usuario)
    await db.commit()

    return novo_usuario


@router.put('/{usuario_id}', status_code=status.HTTP_200_OK, response_model=UsuarioUpdateSchema)
async def put_usuario(usuario_id: int, usuario: UsuarioUpdateSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up = result.scalar_one_or_none()

        if not usuario_up:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)

        if usuario_up:
            if usuario.nome is not None:
                usuario_up.nome = usuario.nome
            if usuario.email is not None:
                usuario_up.email = usuario.email
            if usuario.telefone is not None:
                usuario_up.telefone = usuario.telefone

            await session.commit()

            return usuario_up


@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del = result.scalar_one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            
            return Response('Usuário apagado com sucesso!')

        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
