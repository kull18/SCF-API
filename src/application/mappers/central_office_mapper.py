from src.domain.schemas.CentralOffice import CentralOfficeCreateSchema
from src.application.dtos.responses.central_office_response import CentralOfficeResponse
from src.domain.models.CentralOffice import CentralOffice
from src.services.geo import point_from_coords, coords_from_point


class CentralOfficeMapper:
    @staticmethod
    def schema_to_model(schema: CentralOfficeCreateSchema) -> CentralOffice:
        return CentralOffice(
            prefix=schema.prefix,
            name=schema.name,
            city=schema.city,
            location=point_from_coords(schema.latitude, schema.longitude),
        )

    @staticmethod
    def model_to_response(model: CentralOffice) -> CentralOfficeResponse:
        latitude, longitude = coords_from_point(model.location)
        return CentralOfficeResponse(
            id=model.id,
            prefix=model.prefix,
            name=model.name,
            city=model.city,
            latitude=latitude,
            longitude=longitude,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )