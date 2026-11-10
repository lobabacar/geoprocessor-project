import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon


@pytest.fixture
def sample_polygon():

    polygon = Polygon(
        [
            (0, 0),
            (100, 0),
            (100, 100),
            (0, 100),
        ]
    )

    return gpd.GeoDataFrame(
        geometry=[polygon],
        crs="EPSG:2950",
    )


@pytest.fixture
def sample_points():

    points = [
        Point(0, 0),
        Point(100, 100),
        Point(200, 200),
    ]

    return gpd.GeoDataFrame(
        geometry=points,
        crs="EPSG:2950",
    )
