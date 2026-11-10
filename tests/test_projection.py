import geopandas as gpd
import pytest
from shapely.geometry import Point

from geoprocessor.projection import reproject_layer


def test_reprojection():
    # creer une couche geographique de test avec un point
    gdf = gpd.GeoDataFrame(
        {"id": [1]}, geometry=[Point(-71.89, 45.40)], crs="EPSG:4326"
    )
    # reprojeter la couche vers EPSG:2950
    gdf_reprojected = reproject_layer(gdf, target_epsg=2950)
    # verifier que le CRS de la couche reprojetee est correct
    assert gdf_reprojected.crs.to_epsg() == 2950
    # verifie que l'antite est conservee apres la reprojection
    assert len(gdf_reprojected) == 1


def test_missing_crs():
    # creer une couche geographique de test sans CRS
    gdf = gpd.GeoDataFrame({"id": [1]}, geometry=[Point(-71.89, 45.40)], crs=None)
    # verifier que la fonction leve une exception ValueError
    with pytest.raises(
        ValueError, match="La couche ne possède pas de système de coordonnées défini."
    ):
        reproject_layer(gdf, target_epsg=2950)
