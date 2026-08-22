from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository
from src.application.usecases.CreateCentralOfficeUseCase import CreateCentralOfficeUseCase
from src.application.usecases.ListCentralOfficesUseCase import ListCentralOfficesUseCase
from src.application.usecases.GetCentralOfficeUseCase import GetCentralOfficeUseCase
from src.application.usecases.UpdateCentralOfficeUseCase import UpdateCentralOfficeUseCase
from src.application.usecases.DeleteCentralOfficeUseCase import DeleteCentralOfficeUseCase
from src.domain.schemas.CentralOffice import (
    CentralOfficeCreateSchema,
    CentralOfficeUpdateSchema,
)
from src.application.dtos.responses.central_office_response import CentralOfficeResponse
from src.application.mappers.central_office_mapper import CentralOfficeMapper

router = APIRouter(prefix="/central-offices", tags=["central-offices"])


@router.post("", response_model=CentralOfficeResponse, status_code=201)
async def create_central_office(
    schema: CentralOfficeCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = CentralOfficeRepository(session)
    use_case = CreateCentralOfficeUseCase(repository)
    model = CentralOfficeMapper.schema_to_model(schema)
    created = await use_case.execute(model)
    return CentralOfficeMapper.model_to_response(created)


@router.get("", response_model=list[CentralOfficeResponse])
async def list_central_offices(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = CentralOfficeRepository(session)
    use_case = ListCentralOfficesUseCase(repository)
    offices = await use_case.execute()
    return [CentralOfficeMapper.model_to_response(o) for o in offices]


@router.get("/{office_id}", response_model=CentralOfficeResponse)
async def get_central_office(
    office_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = CentralOfficeRepository(session)
    use_case = GetCentralOfficeUseCase(repository)
    office = await use_case.execute(office_id)
    return CentralOfficeMapper.model_to_response(office)


@router.patch("/{office_id}", response_model=CentralOfficeResponse)
async def update_central_office(
    office_id: int,
    schema: CentralOfficeUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = CentralOfficeRepository(session)
    use_case = UpdateCentralOfficeUseCase(repository)
    updated = await use_case.execute(office_id, schema)
    return CentralOfficeMapper.model_to_response(updated)


@router.delete("/{office_id}", status_code=204)
async def delete_central_office(
    office_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = CentralOfficeRepository(session)
    use_case = DeleteCentralOfficeUseCase(repository)
    await use_case.execute(office_id)