from typing import List

from fastapi import Query
from sqlalchemy import select, funcfilter
from sqlalchemy.ext.asyncio import AsyncSession
from models import Launch, Rocket, Mission
from schema.enums import LaunchOrderEnum, MissionOrderEnum, RocketOrderEnum
from database import LocalAsyncSession as async_session

async def get_launches(
    # async_session: AsyncSession,
    order_by: LaunchOrderEnum = LaunchOrderEnum.id,
    page: Query(ge=1, default=1) = 1, size: Query(ge=1, default=5) = 5,
    desc: bool = True,
    ) -> list[Launch]:

    order = None
    match order_by:
        case LaunchOrderEnum.launch_date_utc:
            order = Launch.launch_date_utc
        case _:
            order = Launch.id


    # print(order)
    # print(type(order))
    # print(dir(order))
    desc_or_asc = order.desc() if desc else order.asc()

    async with async_session() as transaction:
        result = await transaction.execute(
            select(Launch).order_by(desc_or_asc).offset(page - 1).limit(size)
        )
        return result.scalars().all()


async def get_successfull_launches(
    # async_session: AsyncSession,
    order_by: LaunchOrderEnum = LaunchOrderEnum.id,
    page: Query(ge=1, default=1) = 1, size: Query(ge=1, default=5) = 5,
    desc: bool = True) -> list[Launch]:

    order = None
    match order_by:
        case LaunchOrderEnum.launch_date_utc:
            order = Launch.launch_date_utc
        case _:
            order = Launch.id

    desc_or_asc = order.desc() if desc else order.asc()

    async with async_session() as transaction:
        result = await transaction.execute(
            funcfilter(
                select(Launch).order_by(desc_or_asc).offset(page - 1).limit(size),
                Launch.launch_success is True
            )
        )
        return result.scalars().all()


async def add_launches(
    # async_session: AsyncSession,
    launches: List[Launch]
    ) -> None:
    async with async_session() as transaction:
        async with transaction.begin():
            # print(dir(transaction))
            transaction.add_all(launches)
            transaction.commit()


async def get_rockets(
    # async_session: AsyncSession,
    order_by: RocketOrderEnum = RocketOrderEnum.id,
    page: Query(ge=1, default=1) = 1,
    size: Query(ge=1, default=5) = 5,
    desc: bool = True,
    ) -> list[Rocket]:

    order = None
    match order_by:
        case RocketOrderEnum.first_flight:
            order = Rocket.first_flight
        case _:
            order = Rocket.id

    desc_or_asc = order.desc() if desc else order.asc()

    async with async_session() as sess:
        result = await sess.execute(
            select(Rocket).order_by(desc_or_asc).offset(page - 1).limit(size)
        )
        return result.scalars().all()


async def add_rockets(
    # async_session: AsyncSession,
    rockets: List[Rocket],
    ) -> None:
    async with async_session() as transaction:
        async with transaction.begin():
            transaction.add_all(rockets)
            await transaction.commit()


async def get_missions(
    # async_session: AsyncSession,
    order_by: MissionOrderEnum = MissionOrderEnum.id,
    page: Query(ge=1, default=1) = 1,
    size: Query(ge=1, default=5) = 5,
    desc: bool = True,
    ) -> list[Mission]:

    order = None
    match order_by:
        case MissionOrderEnum.manufactures:
            order = Mission.manufactures
        case MissionOrderEnum.payloads:
            order = Mission.payloads
        case _:
            order = Mission.id

    desc_or_asc = order.desc() if desc else order.asc()

    async with async_session() as sess:
        result = await sess.execute(
            select(Mission).order_by(desc_or_asc).offset(page - 1).limit(size)
        )
        return result.scalars().all()


async def add_missions(
    # async_session: AsyncSession,
    missions: List[Mission]
    ) -> None:
    async with async_session() as transaction:
        async with transaction.begin():
            transaction.add_all(missions)
            await transaction.commit()
