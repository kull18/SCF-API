from src.domain.schemas.CentralOffice import CentralOfficeUpdateSchema
from src.domain.models.CentralOffice import CentralOffice
from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository
from src.services.geo import point_from_coords, coords_from_point


class UpdateCentralOfficeUseCase:
    def __init__(self, repository: CentralOfficeRepository):
        self._repository = repository

    async def execute(
        self, office_id: int, schema: CentralOfficeUpdateSchema
    ) -> CentralOffice:
        office = await self._repository.get_by_id(office_id)
        if office is None:
            raise ValueError(f"CentralOffice with id={office_id} not found")

        data = schema.model_dump(exclude_unset=True)

        if "latitude" in data or "longitude" in data:
            current_lat, current_lon = coords_from_point(office.location)
            latitude = data.pop("latitude", current_lat)
            longitude = data.pop("longitude", current_lon)
            office.location = point_from_coords(latitude, longitude)

        for field, value in data.items():
            setattr(office, field, value)

        return await self._repository.update(office)