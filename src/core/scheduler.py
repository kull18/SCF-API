import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.core.session import AsyncSessionLocal
from src.infrastructure.repositories.EventRepository import EventRepository
from src.infrastructure.repositories.RevokedTokenRepository import RevokedTokenRepository
from src.infrastructure.repositories.DeviceTokenRepository import DeviceTokenRepository
from src.application.usecases.CloseResolvedEventsUseCase import CloseResolvedEventsUseCase
from src.application.usecases.PurgeExpiredTokensUseCase import PurgeExpiredTokensUseCase

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def close_resolved_events_job() -> None:
    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        use_case = CloseResolvedEventsUseCase(repository)
        closed_count = await use_case.execute()

        if closed_count > 0:
            logger.info(f"Cerrados automaticamente {closed_count} eventos RESOLVED -> CLOSED")


async def purge_expired_tokens_job() -> None:
    async with AsyncSessionLocal() as session:
        revoked_token_repository = RevokedTokenRepository(session)
        device_token_repository = DeviceTokenRepository(session)
        use_case = PurgeExpiredTokensUseCase(revoked_token_repository, device_token_repository)

        result = await use_case.execute()

        if result["revoked_tokens_purged"] or result["device_tokens_purged"]:
            logger.info(
                f"Limpieza de tokens: {result['revoked_tokens_purged']} revoked_tokens, "
                f"{result['device_tokens_purged']} device_tokens eliminados"
            )


def start_scheduler() -> None:
    scheduler.add_job(
        close_resolved_events_job,
        trigger=CronTrigger(hour=3, minute=0),
        id="close_resolved_events",
        replace_existing=True,
    )
    scheduler.add_job(
        purge_expired_tokens_job,
        trigger=CronTrigger(hour=4, minute=0),  # despues del job de eventos, para no competir
        id="purge_expired_tokens",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler iniciado: jobs de cierre automatico y limpieza de tokens registrados")


def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)