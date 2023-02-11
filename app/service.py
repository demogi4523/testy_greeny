from typing import List

from fastapi import Query
from sqlalchemy import select, funcfilter, text

from models import Launch, Rocket, Mission
from schema.enums import LaunchOrderEnum, MissionOrderEnum, RocketOrderEnum
from database import LocalAsyncSession as async_session

async def get_launches(
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

    desc_or_asc = order.desc() if desc else order.asc()

    async with async_session() as transaction:
        result = await transaction.execute(
            select(Launch).order_by(desc_or_asc).offset(page - 1).limit(size)
        )
        return result.scalars().all()


async def get_launch(launch_id: str) -> Launch | None:
    async with async_session() as sess:
        result = await sess.get(Launch, launch_id)
        await sess.commit()
        return result


async def get_successfull_launches(
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
    launches: List[Launch]
    ) -> None:
    async with async_session() as transaction:
        async with transaction.begin():
            transaction.add_all(launches)
            await transaction.commit()


async def get_rockets(
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


async def get_rocket(rocket_id: str) -> Rocket | None:
    async with async_session() as sess:
        result = await sess.get(Rocket, rocket_id)
        await sess.commit()
        return result

async def add_rockets(
    rockets: List[Rocket],
    ) -> None:
    async with async_session() as transaction:
        async with transaction.begin():
            transaction.add_all(rockets)
            await transaction.commit()


async def get_missions(
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


async def get_mission(mission_id: str) -> Mission | None:
    async with async_session() as sess:
        result = await sess.get(Mission, mission_id)
        await sess.commit()
        return result


async def add_missions(
    missions: List[Mission]
    ) -> None:
    async with async_session() as transaction:
        async with transaction.begin():
            transaction.add_all(missions)
            await transaction.commit()
