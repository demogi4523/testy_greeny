import os
from typing import List
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Query
from databases import Database

from config import Config
from schema.dto import (
    Launch,
    Rocket,
    Mission,
)
from schema.enums import (
    LaunchOrderEnum,
    RocketOrderEnum,
    MissionOrderEnum,
)
from script import fill_data_to_db
from service import (
    get_launches,
    get_rockets,
    get_missions,
)


MODE = os.environ.get("MODE", "prod")

dotenv_path = {
    "test": 'env/.env.test',
    "prod": 'env/.env.prod',
    "dev":  'env/.env.dev',
}

load_dotenv(dotenv_path=dotenv_path[MODE])

config = Config()
DATABASE_URL = config.get_db_url()
database = Database(DATABASE_URL)

app = FastAPI()


@app.on_event("startup")
async def startup(
    ) -> None:
    await fill_data_to_db()



@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/")
async def root(request: Request) -> dict:
    base_url = request.base_url
    return {
        "launches": f"{base_url}launches/",
        "rockets": f"{base_url}rockets/",
        "missions": f"{base_url}missions/",
        "docs": f"{base_url}docs/",
    }


@app.get("/launches/", response_model=List[Launch])
async def read_launches(
    order_by: LaunchOrderEnum = "id",
    size: int = 8, page: int = Query(ge=1, default=1), desc: bool = False,
    ) -> List[Launch]:
    return await get_launches(order_by, page, size, desc)


@app.get("/rockets/", response_model=List[Rocket])
async def read_rockets(
    order_by: RocketOrderEnum = "id",
    size: int = 5, page: int = Query(ge=1, default=1), desc: bool = False,
    ) -> List[Rocket]:
    return await get_rockets(order_by, page, size, desc)


@app.get("/missions/", response_model=List[Mission])
async def read_missions(
    order_by: MissionOrderEnum = "id",
    size: int = 3, page: int = Query(ge=1, default=1), desc: bool = False,
    ) -> List[Mission]:
    return await get_missions(order_by, page, size, desc)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=7000)
