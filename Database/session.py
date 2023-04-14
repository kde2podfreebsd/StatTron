import configparser
import os
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

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

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
