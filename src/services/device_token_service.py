import secrets
from datetime import datetime, timedelta, timezone

DEVICE_TOKEN_EXPIRE_DAYS = 90


def generate_device_token() -> str:
    """Token opaco (no JWT) -- solo un identificador aleatorio de alta
    entropia. No lleva informacion codificada, por eso hay que consultar
    la BD para validarlo, a diferencia del access_token normal."""
    return secrets.token_urlsafe(48)


def device_token_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=DEVICE_TOKEN_EXPIRE_DAYS)