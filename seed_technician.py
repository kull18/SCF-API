import asyncio

from src.core.session import AsyncSessionLocal
from src.domain.models.User import User, UserRole
from src.services.password_service import hash_password
from src.services.technician_code_service import generate_technician_code
from src.services.temp_password_service import generate_temp_password

# Importa TODOS los modelos para que SQLAlchemy resuelva las relaciones
# entre clases antes de instanciar cualquier modelo.
from src.domain.models import (  # noqa: F401
    CentralOffice,
    Event,
    EventComment,
    EventPhoto,
    Notification,
    DeviceToken,
    RevokedToken,
)

TECHNICIAN_PHONE = "+525500000000"  # numero ficticio de prueba, no uno real


async def seed_technician():
    async with AsyncSessionLocal() as session:
        temp_password = generate_temp_password()

        technician = User(
            technician_code=generate_technician_code(),
            phone=TECHNICIAN_PHONE,
            role=UserRole.ADMIN,
            password_hash=hash_password(temp_password),
            is_active=True,
            must_change_password=True,
            profile_completed=False,
        )
        session.add(technician)
        await session.commit()
        await session.refresh(technician)

        print("Técnico de prueba creado:")
        print(f"  technician_code: {technician.technician_code}")
        print(f"  phone: {technician.phone}")
        print(f"  password temporal: {temp_password}")


if __name__ == "__main__":
    asyncio.run(seed_technician())