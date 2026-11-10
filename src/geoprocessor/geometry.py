# src/geoprocessor/geometry.py

import geopandas as gpd


def calculate_area(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Ajoute les superficies en hectares et en km²."""

    if gdf.crs is None:
        raise ValueError("CRS non défini.")

    if not gdf.crs.is_projected:
        raise ValueError("Utiliser un système de coordonnées projeté.")

    if gdf.crs.axis_info[0].unit_conversion_factor != 1.0:
        raise ValueError("Le CRS doit utiliser le mètre comme unité.")

    result = gdf.copy()

    result["area_m2"] = result.geometry.area
    result["area_ha"] = result["area_m2"] / 10_000
    result["area_km2"] = result["area_m2"] / 1_000_000

    return result
