import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.core.session import AsyncSessionLocal
from src.infrastructure.repositories.EventRepository import EventRepository
from src.application.usecases.CloseResolvedEventsUseCase import CloseResolvedEventsUseCase

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def close_resolved_events_job() -> None:
    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        use_case = CloseResolvedEventsUseCase(repository)
        closed_count = await use_case.execute()

        if closed_count > 0:
            logger.info(f"Cerrados automaticamente {closed_count} eventos RESOLVED -> CLOSED")


def start_scheduler() -> None:
    scheduler.add_job(
        close_resolved_events_job,
        trigger=CronTrigger(hour=3, minute=0),  # 3:00 AM, una vez al dia
        id="close_resolved_events",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler iniciado: cierre automatico de eventos corre diario a las 03:00")


def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)