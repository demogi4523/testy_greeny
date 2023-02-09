import json
import os
from typing import List

from fastapi import FastAPI, Request, Query
from dotenv import load_dotenv

from database import get_db
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
from models import (
    get_launches,
    get_rockets,
    get_missions,
)

load_dotenv()


db_user = os.environ["POSTGRES_USER"]
db_passwd = os.environ["POSTGRES_PASSWORD"]
db_name = os.environ["POSTGRES_DB"]
if os.environ.get("MODE") == "TESTING":
    db_host = os.environ["POSTGRES_HOST"]
    db_port = os.environ["POSTGRES_PORT"]
else:
    db_host = "localhost"
    db_port = 5244

DATABASE_URL = f"postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"

database, metadata = get_db(DATABASE_URL)
launches = get_launches(metadata)
rockets = get_rockets(metadata)
missions = get_missions(metadata)

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/")
async def root(request: Request) -> json:
    base_url = request.base_url
    return {
        "launches": f"{base_url}launches/",
        "rockets": f"{base_url}rockets/",
        "missions": f"{base_url}missions/",
    }


@app.get("/launches/", response_model=List[Launch])
async def read_launches(
    order_by: LaunchOrderEnum = "id",
    size: int = 8, page: int = Query(ge=1, default=1), desc: bool = False
    ) -> List[Launch]:
    # FIXME: add desc and asc
    query = launches.select().order_by(order_by).offset(page - 1).limit(size)
    return await database.fetch_all(query)


@app.get("/rockets/", response_model=List[Rocket])
async def read_rockets(
    order_by: RocketOrderEnum = "id",
    size: int = 5, page: int = Query(ge=1, default=1), desc: bool = False
    ) -> List[Rocket]:
    # FIXME: add desc and asc
    query = rockets.select().order_by(order_by).offset(page - 1).limit(size)
    return await database.fetch_all(query)


@app.get("/missions/", response_model=List[Mission])
async def read_missions(
    order_by: MissionOrderEnum = "id",
    size: int = 3, page: int = Query(ge=1, default=1), desc: bool = False
    ) -> List[Mission]:
    # FIXME: add desc and asc
    query = missions.select().order_by(order_by).offset(page - 1).limit(size)
    return await database.fetch_all(query)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=7000)
