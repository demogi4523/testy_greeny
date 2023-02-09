import os
import asyncio

import typer
from databases import Database
from dotenv import load_dotenv

from script import run

load_dotenv()

db_user = os.environ["POSTGRES_USER"]
db_passwd = os.environ["POSTGRES_PASSWORD"]
db_host = os.environ["POSTGRES_HOST"]
db_name = os.environ["POSTGRES_DB"]
db_port = os.environ["POSTGRES_PORT"]

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"

cli = typer.Typer()
database = Database(DATABASE_URL)


@cli.command()
async def fill_db():
    return await run()

if __name__ == "__main__":
    # FIXME: module cli not working
    asyncio.run(fill_db())

