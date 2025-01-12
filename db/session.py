from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .interface import db


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a database session."""
    async for session in db.get_session():
        yield session
