import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from geoprocessor.exceptions import GeoGeometryError
from geoprocessor.processor import GeoProcessor


def test_valid_geometry(tmp_path):

    polygon = Polygon(
        [
            (0, 0),
            (100, 0),
            (100, 100),
            (0, 100),
        ]
    )

    gdf = gpd.GeoDataFrame(
        geometry=[polygon],
        crs="EPSG:2950",
    )

    processor = GeoProcessor(tmp_path / "zones.gpkg")

    processor.gdf = gdf

    result = processor.validate_geometry()

    assert result == 1


def test_invalid_geometry(tmp_path):

    # Polygone avec auto-intersection
    polygon = Polygon(
        [
            (0, 0),
            (100, 100),
            (100, 0),
            (0, 100),
            (0, 0),
        ]
    )

    gdf = gpd.GeoDataFrame(
        geometry=[polygon],
        crs="EPSG:2950",
    )

    processor = GeoProcessor(tmp_path / "zones.gpkg")

    processor.gdf = gdf

    with pytest.raises(GeoGeometryError):
        processor.validate_geometry()


def test_geometry_without_load(tmp_path):

    processor = GeoProcessor(tmp_path / "zones.gpkg")

    with pytest.raises(RuntimeError):
        processor.validate_geometry()
