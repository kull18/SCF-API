from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point


def point_from_coords(latitude: float, longitude: float):
    """Point(x, y) = Point(longitude, latitude), not the other way around."""
    return from_shape(Point(longitude, latitude), srid=4326)


def coords_from_point(location) -> tuple[float, float]:
    """Returns (latitude, longitude)."""
    point = to_shape(location)
    return point.y, point.x