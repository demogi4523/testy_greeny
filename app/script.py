import os
from datetime import datetime, date
import asyncio

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from databases import Database
from dotenv import load_dotenv
from dateutil import parser

from models import get_launches, get_rockets, get_missions


# TODO: refactor this module
space_x_url = "https://spacex-production.up.railway.app/"
transport = AIOHTTPTransport(url=space_x_url)

client = Client(transport=transport, fetch_schema_from_transport=True)

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

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"

metadata = MetaData()

db_launches = get_launches(metadata)
db_rockets = get_rockets(metadata)
db_missions = get_missions(metadata)

Base = declarative_base(metadata=metadata)


async def launches_query_async(client):
    query = gql(
        """
        query LaunchesQuery {
            launches {
                id,
                details,
                launch_date_utc,
                launch_success,
                upcoming,
            }
        }
        """
    )
    res = await client.execute_async(query)
    launches = res["launches"]
    launches = [{
        **launch,
        "launch_date_utc": parser.parse(launch["launch_date_utc"]),
    } for launch in launches]

    return launches


async def rockets_query_async(client):
    query = gql(
        """
        query RocketsQuery {
            dragons {
                id,
                name,
                first_flight,
                diameter {
                    feet,
                },
                launch_payload_mass {
                    lb,
                },
            }
        }
        """
    )
    res = await client.execute_async(query)
    rockets = res["dragons"]
    rockets = [{
        **rocket,
        "first_flight": parser.parse(rocket["first_flight"]).date(),
        "diameter": rocket["diameter"]["feet"],
        "launch_payload_mass": rocket["launch_payload_mass"]["lb"]
    } for rocket in rockets]

    return rockets


async def missions_query_async(client):
    query = gql(
        """
        query MissionsQuery {
            missions {
                id,
                name,
                website,
                manufacturers,
                payloads {
                    orbit,
                    nationality,
                    manufacturer,
                },
            }
        }
        """
    )
    res = await client.execute_async(query)
    missions = res["missions"]


    missions = [{
        **mission,
        "payloads": "orbit: {}\nnationality: {}\nmanufacturer: {}".format(
                mission['payloads']['orbit'],
                mission['payloads']['nationality'],
                mission['payloads']['manufacturer'],
            )
    } for mission in missions]

    return missions

async def init_models():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

async def run():
    launches = await launches_query_async(client)
    rockets = await rockets_query_async(client)
    missions = await missions_query_async(client)

    database = Database(DATABASE_URL)
    await init_models()
    await database.connect()

    query = db_launches.insert()
    await database.execute_many(query, launches)

    query = db_rockets.insert()
    await database.execute_many(query, rockets)

    query = db_missions.insert()
    await database.execute_many(query, missions)

    await database.disconnect()

if __name__ =='__main__':
    asyncio.run(run())
