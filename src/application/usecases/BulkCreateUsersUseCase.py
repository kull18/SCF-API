from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.password_service import hash_password
from src.services.technician_code_service import generate_technician_code
from src.services.temp_password_service import generate_temp_password
from src.services.whatsapp_service import send_credentials_whatsapp

MAX_CODE_ATTEMPTS = 10


class BulkCreateUsersUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, phones: list[str]) -> list[dict]:
        results = []

        for phone in phones:
            technician_code = await self._generate_unique_technician_code()
            temp_password = generate_temp_password()

            user = User(
                technician_code=technician_code,
                phone=phone,
                role=UserRole.TECNICO,
                password_hash=hash_password(temp_password),
                must_change_password=True,
                profile_completed=False,
            )

            created = await self._repository.create(user)

            whatsapp_sent = await send_credentials_whatsapp(
                phone=phone,
                technician_code=technician_code,
                temp_password=temp_password,
            )

            results.append({
                "id": created.id,
                "technician_code": created.technician_code,
                "phone": created.phone,
                "temp_password": temp_password,
                "whatsapp_sent": whatsapp_sent,
            })

        return results

    async def _generate_unique_technician_code(self) -> str:
        for _ in range(MAX_CODE_ATTEMPTS):
            code = generate_technician_code()
            existing = await self._repository.get_by_technician_code(code)
            if existing is None:
                return code
        raise RuntimeError("Could not generate a unique technician_code")