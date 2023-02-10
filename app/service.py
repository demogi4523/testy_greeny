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


    print(order)
    print(type(order))
    print(dir(order))
    desc_or_asc = order.desc() if desc else order.asc()

    async with async_session() as q:
        result = await q.execute(
            select(Launch).order_by(desc_or_asc).offset(page).limit(size)
        )
        return result.scalars().all()


async def get_successfull_launches(
    session: AsyncSession, order_by: LaunchOrderEnum = LaunchOrderEnum.id,
    page: Query(ge=1, default=1) = 1, size: Query(ge=1, default=5) = 5,
    desc: bool = True) -> list[Launch]:

    order = {
        LaunchOrderEnum.id: Launch.id,
        LaunchOrderEnum.launch_date_utc: Launch.launch_date_utc,
    }
    desc_or_asc = order[order_by].desc() if desc else order[order_by].asc()

    result = await session.execute(
        funcfilter(
            select(Launch).order_by(desc_or_asc).offset(page).limit(size),
            Launch.launch_success == True
        )
    )
    return result.scalars().all()


async def add_launches(session: AsyncSession, launches: List[Launch]) -> None:
    # async with session as sess:
        # for launch in launches:
    print(dir(session))
    async with session.begin() as q:
        print(dir(q))
        q.add_all(launches)
        q.commit()
    # await session.commit()
    # await session.commit()




async def get_rockets(
    session: AsyncSession, order_by: RocketOrderEnum = RocketOrderEnum.id,
    page: Query(ge=1, default=1) = 1, size: Query(ge=1, default=5) = 5,
    desc: bool = True) -> list[Rocket]:

    order = {
        RocketOrderEnum.id: Rocket.id,
        RocketOrderEnum.first_flight: Rocket.first_flight,
    }
    desc_or_asc = order[order_by].desc() if desc else order[order_by].asc()

    result = await session.execute(
        select(Rocket).order_by(desc_or_asc).offset(page).limit(size)
    )
    return result.scalars().all()


async def add_rockets(session: AsyncSession, rockets: List[Rocket]) -> None:
    for rocket in rockets:
        session.add(rocket)
    await session.commit()

async def get_missions(
    session: AsyncSession, order_by: MissionOrderEnum = MissionOrderEnum.id,
    page: Query(ge=1, default=1) = 1, size: Query(ge=1, default=5) = 5,
    desc: bool = True) -> list[Mission]:

    order = {
        MissionOrderEnum.id: Mission.id,
        MissionOrderEnum.manufactures: Mission.manufactures,
        MissionOrderEnum.payloads: Mission.payloads,
    }
    desc_or_asc = order[order_by].desc() if desc else order[order_by].asc()

    result = await session.execute(
        select(Mission).order_by(desc_or_asc).offset(page).limit(size)
    )
    return result.scalars().all()


async def add_missions(session: AsyncSession, missions: List[Mission]) -> None:
    for mission in missions:
        session.add(mission)
    await session.commit
