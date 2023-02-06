import os
import asyncio

from sqlalchemy import Column, String, Boolean, MetaData, Table
from databases import Database
from dotenv import load_dotenv

from script import get_launches_async, client
from models import get_launches

load_dotenv()

db_user = os.environ["POSTGRES_USER"]
db_passwd = os.environ["POSTGRES_PASSWORD"]
db_host = "localhost"
db_name = os.environ["POSTGRES_DB"]
db_port = 5244

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"


# FIXME: create usual tests for pytest
metadata = MetaData()

db_launches = get_launches()

missions = [{
        "id": "asg",
        "name": "Lesly",
        "website": "https://qq.com",
        "manufactures": "mfs",
        "payloads": {
            "orbit": "ss",
            "nationality": "asf",
            "manufacturer": "asgs",
        },
    },
    ]

async def main():
    launches = await get_launches_async(client)

    database = Database(DATABASE_URL)
    await database.connect()

    query = db_launches.delete()
    # query = "DELETE FROM launches;"
    await database.execute(query=query)

    query = db_launches.insert()
    await database.execute_many(query=query, values=launches)
    await database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())

