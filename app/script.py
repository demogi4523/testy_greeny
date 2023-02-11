import asyncio

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from databases import Database
from dateutil import parser

from database import Base, DATABASE_URL, engine
from models import (
    Launch as LaunchDB,
    Rocket as RocketDB,
    Mission as MissionDB,
)
from service import add_launches, add_missions, add_rockets


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
                mission_id,
                rocket {
                    rocket {
                        id,
                    },
                },
            }
        }
        """
    )
    res = await client.execute_async(query)
    launches = res["launches"]

    for ind, launch in enumerate(launches):
        ldu = parser.parse(launch["launch_date_utc"])
        rid = launch["rocket"]["rocket"]["id"]
        mid = launch["mission_id"][0]
        del launches[ind]['rocket']
        launches[ind]["launch_date_utc"] = ldu
        launches[ind]["rocket_id"] = rid
        launches[ind]["mission_id"] = mid


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
        "payloads": "orbit: {}\nnationality: {}\nmanufacturer: {}".format( # pylint: disable=consider-using-f-string
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

async def fill_data_to_db():
    database = Database(DATABASE_URL)
    await init_models()
    await database.connect()

    launches = await launches_query_async(gql_client)
    launches = [LaunchDB(**l) for l in launches]
    await add_launches(launches)

    rockets = await rockets_query_async(gql_client)
    rockets = [RocketDB(**r) for r in rockets]
    await add_rockets(rockets)

    missions = await missions_query_async(gql_client)
    missions = [MissionDB(**m) for m in missions]
    await add_missions(missions)

    await database.disconnect()

if __name__ =='__main__':
    asyncio.run(fill_data_to_db())
