import asyncio
from fastapi import Depends

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from databases import Database
from dotenv import load_dotenv
from dateutil import parser

from config import Config
from database import get_session, Base, DATABASE_URL, engine
from models import Launch, Mission, Rocket
from service import add_launches, add_missions, add_rockets


# TODO: refactor this module
# async_session = get_session()

SPACE_X_URL = "https://spacex-production.up.railway.app/"
transport = AIOHTTPTransport(url=SPACE_X_URL)

gql_client = Client(transport=transport, fetch_schema_from_transport=True)

async def launches_query_async(client: Client):
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


async def rockets_query_async(client: Client):
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


async def missions_query_async(client: Client):
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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def run(async_session: AsyncSession = Depends(get_session)):
    launches = await launches_query_async(gql_client)
    rockets = await rockets_query_async(gql_client)
    missions = await missions_query_async(gql_client)

    database = Database(DATABASE_URL)
    await init_models()
    await database.connect()


    print(type(async_session))
    await add_launches(async_session, launches)
    # await add_rockets(async_session, rockets)
    # await add_missions(async_session, missions)

    await database.disconnect()

if __name__ =='__main__':
    asyncio.run(run())
