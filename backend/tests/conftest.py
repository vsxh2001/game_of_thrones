import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy import text
from app.main import app
from app.db.session import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/got_test"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True, echo=True)

# Create test session factory
test_async_session = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_setup():
    """Set up test database."""
    # Create tables
    async with test_engine.begin() as conn:
        # Drop all existing tables
        await conn.run_sync(lambda x: x.execute(text("DROP SCHEMA public CASCADE")))
        await conn.run_sync(lambda x: x.execute(text("CREATE SCHEMA public")))

        # Create tables from schema.sql
        with open("schema.sql", "r") as f:
            schema = f.read()
            await conn.execute(text(schema))

    yield test_engine

    # Cleanup after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(lambda x: x.execute(text("DROP SCHEMA public CASCADE")))
        await conn.run_sync(lambda x: x.execute(text("CREATE SCHEMA public")))


@pytest.fixture
async def db_session():
    """Get test database session."""
    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture
def client() -> Generator:
    """Get test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Get async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
