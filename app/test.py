import asyncio
import os

from sqlalchemy import MetaData
from databases import Database
from dotenv import load_dotenv

from script import launches_query_async, gql_client
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

db_launches = get_launches(metadata=metadata)

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

async def main() -> None:
    launches = await launches_query_async(gql_client)

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
