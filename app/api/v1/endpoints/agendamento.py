from typing import List

from fastapi import APIRouter, Response, HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.agendamento_model import AgendamentoModel
from schemas.agendamento_schema import AgendamentoSchema, AgendamentoSchemaBase, AgendamentoUpdateSchema
from models.servico_model import ServicoModel
from models.barbeiro_model import BarbeiroModel

from core.deps import get_session

from datetime import timedelta


router = APIRouter()


@router.get('/{agendamento_id}', status_code=status.HTTP_200_OK, response_model=AgendamentoSchemaBase)
async def get_agendamento(agendamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id)
        result = await session.execute(query)
        agendamento = result.scalar_one_or_none()

        if agendamento:
            return agendamento
        else:
            raise HTTPException(detail='Agendamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[AgendamentoSchemaBase])
async def get_agendamentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendamentoModel)
        result = await session.execute(query)
        agendamentos: List[AgendamentoModel] = result.scalars().unique().all()

        return agendamentos


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AgendamentoSchema)
async def post_agendamento(agendamento: AgendamentoSchemaBase, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == agendamento.servico_id)
        result = await session.execute(query)
        servico = result.scalar_one_or_none()

        if not servico:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Serviço não encontrado')

        data_hora_fim = (agendamento.data_hora_inicio + timedelta(minutes=servico.duracao_minutos))

        novo_agendamento = AgendamentoModel(
            data_hora_inicio=agendamento.data_hora_inicio,
            data_hora_fim=data_hora_fim,
            confirmado=True,
            usuario_id=agendamento.usuario_id,
            barbeiro_id=agendamento.barbeiro_id,
            servico_id=agendamento.servico_id,
        )

        db.add(novo_agendamento)
        await db.commit()

        return novo_agendamento


@router.put('/{agendamento_id}', status_code=status.HTTP_200_OK, response_model=AgendamentoUpdateSchema)
async def put_agendamento(agendamento_id: int, agendamento: AgendamentoUpdateSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id)
        result = await session.execute(query)
        agendamento_up: AgendamentoModel = result.scalars().unique().one_or_none()

        if not agendamento_up:
            raise HTTPException(detail='Agendamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)

        if agendamento.data_hora_inicio is not None:
            agendamento_up.data_hora_inicio = agendamento.data_hora_inicio

        if agendamento.confirmado is not None:
            agendamento_up.confirmado = agendamento.confirmado

        if agendamento.servico_id is not None:
            query = select(ServicoModel).filter(ServicoModel.id == agendamento.servico_id)
            result = await session.execute(query)
            servico = result.scalar_one_or_none()

            if not servico:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Serviço não encontrado')

            agendamento_up.servico_id = agendamento.servico_id
            agendamento_up.data_hora_fim = (agendamento_up.data_hora_inicio + timedelta(minutes=servico.duracao_minutos))
            
        if agendamento.data_hora_inicio is not None:
            query = select(ServicoModel).filter(ServicoModel.id == agendamento_up.servico_id)
            result = await session.execute(query)
            servico = result.scalar_one_or_none()

            if not servico:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Serviço não encontrado')

            agendamento_up.data_hora_fim = (agendamento_up.data_hora_inicio + timedelta(minutes=servico.duracao_minutos))

        if agendamento.barbeiro_id is not None:
            query = select(BarbeiroModel).filter(BarbeiroModel.id == agendamento.barbeiro_id)
            result = await session.execute(query)
            barbeiro = result.scalar_one_or_none()

            if not barbeiro:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barbeiro não encontrado')

            agendamento_up.barbeiro_id = agendamento.barbeiro_id

        await session.commit()

        return agendamento_up


@router.delete('/{agendamento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_agendamento(agendamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id)
        result = await session.execute(query)
        agendamento_del = result.scalar_one_or_none()

        if agendamento_del:
            await session.delete(agendamento_del)
            await session.commit()
            
            return Response('Agendamento apagado com sucesso!')

        else:
            raise HTTPException(detail='Agendamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
