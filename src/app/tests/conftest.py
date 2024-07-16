import asyncio
from typing import Iterator

import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from odmantic.session import AIOSession

from app.api.deps import get_session
from app.core.config import CONFIG
from app.main import main_app
from app.tests.functional.fixtures import *  # noqa
from app.tests.unit.fixtures import *  # noqa

TEST_DATABASE = "testdb_test"


@pytest_asyncio.fixture(scope="session")
async def motor_client():
    motor_client = AsyncIOMotorClient(  # type:ignore
        host=CONFIG.mongo.host,
        port=CONFIG.mongo.port,
        username=CONFIG.mongo.username,
        password=CONFIG.mongo.password,
    )
    yield motor_client
    motor_client.close()


@pytest_asyncio.fixture(scope="session")
async def async_session(motor_client):
    client = motor_client
    client.get_io_loop = asyncio.get_running_loop
    test_engine = AIOEngine(client=client, database=TEST_DATABASE)

    async with test_engine.session() as session:
        yield session
    await client.drop_database(TEST_DATABASE)


@pytest_asyncio.fixture
async def client(async_session: Iterator[AIOSession]):
    def _get_db_override() -> Iterator[AIOSession]:
        return async_session  # pragma: no cover

    main_app.dependency_overrides[get_session] = _get_db_override

    async with AsyncClient(app=main_app, base_url=CONFIG.api.host) as client:
        yield client
