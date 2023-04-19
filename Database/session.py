# import asyncio
import configparser
import os
from typing import Generator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from Database.DAL.ChannelDAL import ChannelDAL


basedir = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(f"{basedir}/../config.ini")

REAL_DATABASE_URL = f"postgresql+asyncpg://{config['POSTGRESQL']['user']}:{config['POSTGRESQL']['password']}@{config['POSTGRESQL']['host']}:{config['POSTGRESQL']['port']}/{config['POSTGRESQL']['database']}"
TEST_DATABASE_URL = f"postgresql+asyncpg://{config['POSTGRESQL_TEST']['user']}:{config['POSTGRESQL_TEST']['password']}@{config['POSTGRESQL_TEST']['host']}:{config['POSTGRESQL_TEST']['port']}/{config['POSTGRESQL_TEST']['database']}"

engine = create_async_engine(
    REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async_session = async_sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def get_db2() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def test():

    async with async_session() as session:
        async with session.begin():

            new_channel = ChannelDAL(session)

            await new_channel.create_channel(
                id_channel=1,
                name="from_parse",
                link="from_parse.link",
                avatar_url="from_parse.avatar_url",
                description="from_parse.description",
                subs_total=4,
            )


# asyncio.run(test())
