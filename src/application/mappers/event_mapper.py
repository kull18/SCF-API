from src.domain.schemas.Event import EventCreateSchema
from src.application.dtos.responses.event_response import (
    EventResponse,
    CentralOfficeSummaryResponse,
)
from src.application.mappers.event_photo_mapper import EventPhotoMapper
from src.domain.models.Event import Event, EventType, EventStatus
from src.domain.models.CentralOffice import CentralOffice
from src.services.geo import point_from_coords, coords_from_point


class EventMapper:
    @staticmethod
    def schema_to_model(schema: EventCreateSchema, reported_by_id: int) -> Event:
        return Event(
            type=EventType.FIBER_CUT,
            origin_office_id=schema.origin_office_id,
            destination_office_id=schema.destination_office_id,
            location=point_from_coords(schema.latitude, schema.longitude),
            location_method=schema.location_method,
            accuracy=schema.accuracy,
            distance_to_origin=0,
            distance_to_destination=0,
            field_reference=schema.field_reference,
            description=schema.description,
            status=EventStatus.ACTIVE,
            reported_by_id=reported_by_id,
        )

    @staticmethod
    def model_to_response(
        model: Event, origin_office: CentralOffice, destination_office: CentralOffice
    ) -> EventResponse:
        latitude, longitude = coords_from_point(model.location)
        return EventResponse(
            id=model.id,
            type=model.type,
            origin_office=CentralOfficeSummaryResponse(
                id=origin_office.id,
                prefix=origin_office.prefix,
                name=origin_office.name,
                city=origin_office.city,
            ),
            destination_office=CentralOfficeSummaryResponse(
                id=destination_office.id,
                prefix=destination_office.prefix,
                name=destination_office.name,
                city=destination_office.city,
            ),
            latitude=latitude,
            longitude=longitude,
            location_method=model.location_method,
            accuracy=model.accuracy,
            distance_to_origin=model.distance_to_origin,
            distance_to_destination=model.distance_to_destination,
            field_reference=model.field_reference,
            description=model.description,
            status=model.status,
            reported_by_id=model.reported_by_id,
            reported_at=model.reported_at,
            photos=[EventPhotoMapper.model_to_response(p) for p in (model.photos or [])],
        )