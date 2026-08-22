from fastapi import Request, HTTPException, Depends
from src.domain.models.User import UserRole, User
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.session import get_session
from src.infrastructure.repositories.UserRepository import UserRepository



def require_role(*allowed_roles: UserRole):
    def dependency(request: Request) -> str:
        role = getattr(request.state, "role", None)

        if role is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if role not in {r.value for r in allowed_roles}:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return role

    return dependency

async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> User:
    technician_code: str | None = getattr(request.state, "technician_code", None)

    if technician_code is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    repository = UserRepository(session)
    user = await repository.get_by_technician_code(technician_code)

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user