import logging
from sqlalchemy import text
from src.core.base import Base
from src.core.session import engine
from src.domain.models import CentralOffice, User, Event, EventPhoto  # noqa: F401

logger = logging.getLogger(__name__)


async def init_db() -> None:
    async with engine.begin() as conn:
        logger.info("Ensuring PostGIS extension exists...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))

        logger.info("Checking for missing tables and creating them if needed...")
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database ready.")