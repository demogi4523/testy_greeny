import os
from typing import List
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, Request, Query
from databases import Database

from config import Config
from database import (
    LocalAsyncSession as AsyncSession,
    engine,
    get_session,
    init_models
)
from schema.dto import (
    Launch,
    Rocket,
    Mission,
)
from models import (
    Launch as LaunchDB,
    Rocket as RocketDB,
    Mission as MissionDB,
)
from schema.enums import (
    LaunchOrderEnum,
    RocketOrderEnum,
    MissionOrderEnum,
)
from service import (
    add_launches,
    add_missions,
    add_rockets,
    get_launches,
    # get_successfull_launches,
    get_rockets,
    get_missions,
)
from script import (
    gql_client,
    launches_query_async,
    missions_query_async,
    rockets_query_async,
)

# MODE = os.environ.get("MODE", "prod")
MODE = os.environ.get("MODE", "dev")

dotenv_path = {
    "test": '.env.test',
    "prod": '.env.prod',
    "dev":  '.env.dev',
}

load_dotenv(dotenv_path=dotenv_path[MODE])

config = Config()
DATABASE_URL = config.get_db_url()
print((DATABASE_URL, MODE))
database = Database(DATABASE_URL)

app = FastAPI()


@app.on_event("startup")
async def startup(
    # async_session: AsyncSession = Depends(get_session),
    ) -> None:
    await database.connect()
    await init_models()

    launches = await launches_query_async(gql_client)
    launches = [LaunchDB(**l) for l in launches]
    await add_launches(launches)
    # await add_launches(async_session, launches)

    rockets = await rockets_query_async(gql_client)
    rockets = [RocketDB(**r) for r in rockets]
    await add_rockets(rockets)

    missions = await missions_query_async(gql_client)
    missions = [MissionDB(**m) for m in missions]
    await add_missions(missions)


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/")
async def root(request: Request) -> dict:
# async def root(request: Request):
    base_url = request.base_url
    return {
        "launches": f"{base_url}launches/",
        "rockets": f"{base_url}rockets/",
        "missions": f"{base_url}missions/",
    }


@app.get("/launches/", response_model=List[Launch])
async def read_launches(
    async_session: AsyncSession = Depends(get_session),
    order_by: LaunchOrderEnum = "id",
    size: int = 8, page: int = Query(ge=1, default=1), desc: bool = False,
    ) -> List[Launch]:
    # return await get_launches(async_session, order_by, page, size, desc)
    return await get_launches(order_by, page, size, desc)


@app.get("/rockets/", response_model=List[Rocket])
async def read_rockets(
    order_by: RocketOrderEnum = "id",
    size: int = 5, page: int = Query(ge=1, default=1), desc: bool = False,
    # async_session: AsyncSession = Depends(get_session),
    ) -> List[Rocket]:
    # return await get_rockets(async_session, order_by, page, size, desc)
    return await get_rockets(order_by, page, size, desc)


@app.get("/missions/", response_model=List[Mission])
async def read_missions(
    order_by: MissionOrderEnum = "id",
    size: int = 3, page: int = Query(ge=1, default=1), desc: bool = False,
    # async_session: AsyncSession = Depends(get_session),
    ) -> List[Mission]:
    # return await get_missions(async_session, order_by, page, size, desc)
    return await get_missions(order_by, page, size, desc)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=7000)
