import geopandas as gpd

from geoprocessor.processor import GeoProcessor


def test_geopackage_workflow(tmp_path, sample_polygon):

    input_path = tmp_path / "input.gpkg"
    output_path = tmp_path / "output.gpkg"

    # Créer un GeoPackage temporaire
    sample_polygon.to_file(
        input_path,
        driver="GPKG",
    )

    # Charger les données
    processor = GeoProcessor(input_path)
    processor.load()

    assert processor.feature_count == 1

    # Reprojeter
    processor.reproject(32198)

    assert processor.gdf.crs.to_epsg() == 32198

    # Calculer les superficies
    processor.add_area()

    assert "area_m2" in processor.gdf.columns

    # Exporter
    processor.export(output_path)

    assert output_path.exists()

    # Relire le résultat
    result = gpd.read_file(output_path)

    assert len(result) == 1
    assert "area_ha" in result.columns
    assert result.crs.to_epsg() == 32198
