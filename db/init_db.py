import asyncio
import logging
from .interface import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Initialize the database."""
    try:
        logger.info("Creating database tables...")
        await db.drop_database()  # Drop existing tables
        await db.create_database()  # Create new tables
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def init() -> None:
    """Initialize database (synchronous wrapper)."""
    asyncio.run(init_db())


if __name__ == "__main__":
    init()
