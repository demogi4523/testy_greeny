import os
from typing import List

from fastapi import FastAPI, Request
from dotenv import load_dotenv

from database import get_db
from schema import (
    Launch,
    Rocket,
    Mission,
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
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root(request: Request):
    raw_url = request.url._url
    return {
        "launches": f"{raw_url}launches/",
        "rockets": f"{raw_url}rockets/",
        "missions": f"{raw_url}missions/",
    }


@app.get("/launches/", response_model=List[Launch])
async def read_launches(order_by: str = "id", size: int = 8, page: int = 1, desc: bool = False):
    # FIXME: add desc and asc
    query = launches.select().order_by(order_by).offset(page).limit(size)
    return await database.fetch_all(query)


@app.get("/rockets/", response_model=List[Rocket])
async def read_rockets(order_by: str = "id", size: int = 5, page: int = 1, desc: bool = False):
    # FIXME: add desc and asc
    query = rockets.select().order_by(order_by).offset(page).limit(size)
    return await database.fetch_all(query)


@app.get("/missions/", response_model=List[Mission])
async def read_missions(order_by: str = "id", size: int = 3, page: int = 1, desc: bool = False):
    # FIXME: add desc and asc
    query = missions.select().order_by(order_by).offset(page).limit(size)
    return await database.fetch_all(query)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=7000)
