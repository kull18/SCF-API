from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.infrastructure.repositories.EventPhotoRepository import EventPhotoRepository
from src.infrastructure.repositories.EventRepository import EventRepository
from src.application.usecases.CreateEventPhotoUseCase import CreateEventPhotoUseCase
from src.application.usecases.ListEventPhotosUseCase import ListEventPhotosUseCase
from src.domain.schemas.EventPhoto import EventPhotoCreateSchema
from src.application.dtos.responses.event_photo_response import EventPhotoResponse
from src.application.mappers.event_photo_mapper import EventPhotoMapper

router = APIRouter(prefix="/event-photos", tags=["event-photos"])


@router.post("", response_model=EventPhotoResponse, status_code=201)
async def create_event_photo(
    schema: EventPhotoCreateSchema, session: AsyncSession = Depends(get_session)
):
    photo_repository = EventPhotoRepository(session)
    event_repository = EventRepository(session)
    use_case = CreateEventPhotoUseCase(photo_repository, event_repository)

    try:
        model = EventPhotoMapper.schema_to_model(schema)
        created = await use_case.execute(model)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return EventPhotoMapper.model_to_response(created)


@router.get("/event/{event_id}", response_model=list[EventPhotoResponse])
async def list_event_photos(event_id: int, session: AsyncSession = Depends(get_session)):
    repository = EventPhotoRepository(session)
    use_case = ListEventPhotosUseCase(repository)

    photos = await use_case.execute(event_id)
    return [EventPhotoMapper.model_to_response(p) for p in photos]