# src/geoprocessor/projection.py

import geopandas as gpd


def reproject_layer(gdf: gpd.GeoDataFrame, target_epsg: int = 2950) -> gpd.GeoDataFrame:
    """
    Reprojette une couche géographique.

    Parameters
    ----------
    gdf : GeoDataFrame
        Couche géographique en entrée.
    target_epsg : int
        Code EPSG du système cible.

    Returns
    -------
    GeoDataFrame
        Couche reprojetée.
    """

    if gdf.crs is None:
        raise ValueError("La couche ne possède pas de système de coordonnées défini.")

    return gdf.to_crs(epsg=target_epsg)
