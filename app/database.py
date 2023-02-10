from typing import AsyncIterator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import Config


config = Config()
DATABASE_URL = config.get_db_url()


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
LocalAsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncIterator[AsyncSession]:
    async with LocalAsyncSession() as session:
        yield session
        # await session.commit()
