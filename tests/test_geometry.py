import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from geoprocessor.exceptions import GeoGeometryError
from geoprocessor.processor import GeoProcessor


def test_validate_geometry():

    # 1. Premier polygone valide
    polygon1 = Polygon(
        [
            (0, 0),
            (100, 0),
            (100, 100),
            (0, 100),
            (0, 0),
        ]
    )

    # 2. Deuxième polygone valide
    polygon2 = Polygon(
        [
            (200, 200),
            (300, 200),
            (300, 300),
            (200, 300),
            (200, 200),
        ]
    )

    # 3. Polygone invalide : auto-intersection
    polygon3 = Polygon(
        [
            (400, 400),
            (500, 500),
            (500, 400),
            (400, 500),
            (400, 400),
        ]
    )

    # 4. Créer le GeoDataFrame
    gdf = gpd.GeoDataFrame(
        geometry=[polygon1, polygon2, polygon3],
        crs="EPSG:2950",
    )

    # 5. Instancier GeoProcessor
    processor = GeoProcessor("data/test.gpkg")

    # 6. Injecter les données
    processor.gdf = gdf

    # Vérifier les géométries avant validation
    assert len(gdf) == 3
    assert int(gdf.geometry.is_valid.sum()) == 2
    assert int((~gdf.geometry.is_valid).sum()) == 1

    # Vérifier l'exception
    with pytest.raises(GeoGeometryError) as exc_info:
        processor.validate_geometry()

    # Vérifier le message
    message = str(exc_info.value)

    assert "1 géométries invalides" in message
    assert "3 entités" in message
