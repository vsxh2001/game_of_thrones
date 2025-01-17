import pytest
from typing import AsyncGenerator, Generator
import asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import asyncpg

from backend.app.main import app
from backend.app.core.config import settings
from db.interface import DatabaseInterface
from db.session import get_db
from db.models.base import Base

# Test database settings
TEST_POSTGRES_DB = "got_championship_test"
TEST_POSTGRES_PORT = "5433"
TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"

# Create test database interface
test_db = DatabaseInterface(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def create_test_database() -> None:
    """Create test database if it doesn't exist."""
    sys_conn = await asyncpg.connect(
        database="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        port=int(TEST_POSTGRES_PORT),  # Use test port
    )
    try:
        await sys_conn.execute(f'CREATE DATABASE "{TEST_POSTGRES_DB}"')
    except asyncpg.exceptions.DuplicateDatabaseError:
        pass
    finally:
        await sys_conn.close()


async def init_test_db() -> None:
    """Initialize test database with schema."""
    await create_test_database()
    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    """Setup test database before each test."""
    await init_test_db()
    yield
    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get test database session."""
    async with test_db.async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override get_db dependency for tests."""
    async with test_db.async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Get test client."""
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as client:
        yield client
    app.dependency_overrides.clear()
