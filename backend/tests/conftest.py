import asyncio
import os

import asyncpg
import pytest

from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from sqlalchemy.pool import NullPool


TEST_DB_NAME = os.getenv(
    "TEST_DB_NAME",
    "greenops_ai_test",
)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    (
        "postgresql+asyncpg://"
        f"localhost/{TEST_DB_NAME}"
    ),
)

TEST_DATABASE_ADMIN_URL = os.getenv(
    "TEST_DATABASE_ADMIN_URL",
    (
        "postgresql://"
        f"localhost/{TEST_DB_NAME}"
    ),
)

ADMIN_DATABASE_URL = os.getenv(
    "ADMIN_DATABASE_URL",
    "postgresql://localhost/postgres",
)


# Must be set before importing the app.
os.environ["APP_ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = (
    TEST_DATABASE_URL
)


from fastapi.testclient import TestClient

from app.db import models  # noqa: F401
from app.db.base import Base
from app.main import app


async def _prepare_test_database() -> None:

    admin_connection = (
        await asyncpg.connect(
            ADMIN_DATABASE_URL
        )
    )

    try:
        database_exists = (
            await admin_connection.fetchval(
                """
                SELECT 1
                FROM pg_database
                WHERE datname = $1
                """,
                TEST_DB_NAME,
            )
        )

        if not database_exists:
            await admin_connection.execute(
                (
                    'CREATE DATABASE '
                    f'"{TEST_DB_NAME}"'
                )
            )

    finally:
        await admin_connection.close()


    vector_connection = (
        await asyncpg.connect(
            TEST_DATABASE_ADMIN_URL
        )
    )

    try:
        await vector_connection.execute(
            (
                "CREATE EXTENSION "
                "IF NOT EXISTS vector"
            )
        )

    finally:
        await vector_connection.close()


    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
    )

    try:
        async with test_engine.begin() as connection:

            await connection.run_sync(
                Base.metadata.drop_all
            )

            await connection.run_sync(
                Base.metadata.create_all
            )

    finally:
        await test_engine.dispose()


@pytest.fixture(
    scope="session",
    autouse=True,
)
def prepare_test_database():
    asyncio.run(
        _prepare_test_database()
    )


@pytest.fixture(scope="session")
def client(
    prepare_test_database,
):
    with TestClient(app) as test_client:
        yield test_client