import pytest
from unittest.mock import AsyncMock, patch

from src.application.usecases.LoginUseCase import LoginUseCase, InvalidCredentialsError
from src.domain.models.User import User, UserRole
from src.core.exceptions import ForbiddenError


def _make_user(is_active=True):
    return User(
        id=1, technician_code="FT-8942", phone="+529611234567",
        password_hash="hashed", role=UserRole.TECNICO, is_active=is_active,
        must_change_password=False, profile_completed=True,
    )


@pytest.mark.asyncio
async def test_successful_login_returns_user_and_token():
    repository = AsyncMock()
    repository.get_by_technician_code.return_value = _make_user()

    with patch(
        "src.application.usecases.LoginUseCase.verify_password", return_value=True
    ), patch(
        "src.application.usecases.LoginUseCase.create_access_token", return_value="fake-jwt"
    ):
        use_case = LoginUseCase(repository)
        user, token = await use_case.execute("FT-8942", "correct-password")

    assert token == "fake-jwt"
    assert user.technician_code == "FT-8942"


@pytest.mark.asyncio
async def test_raises_invalid_credentials_when_user_not_found():
    repository = AsyncMock()
    repository.get_by_technician_code.return_value = None

    use_case = LoginUseCase(repository)

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute("FT-0000", "any-password")


@pytest.mark.asyncio
async def test_raises_invalid_credentials_when_password_is_wrong():
    repository = AsyncMock()
    repository.get_by_technician_code.return_value = _make_user()

    with patch(
        "src.application.usecases.LoginUseCase.verify_password", return_value=False
    ):
        use_case = LoginUseCase(repository)

        with pytest.raises(InvalidCredentialsError):
            await use_case.execute("FT-8942", "wrong-password")


@pytest.mark.asyncio
async def test_raises_forbidden_when_user_is_inactive():
    repository = AsyncMock()
    repository.get_by_technician_code.return_value = _make_user(is_active=False)

    with patch(
        "src.application.usecases.LoginUseCase.verify_password", return_value=True
    ):
        use_case = LoginUseCase(repository)

        with pytest.raises(ForbiddenError):
            await use_case.execute("FT-8942", "correct-password")