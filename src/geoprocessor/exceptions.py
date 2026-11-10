class GeoProcessorError(Exception):
    """Exception de base de notre bibliothèque."""


class GeoDataLoadError(GeoProcessorError):
    """Erreur lors du chargement des données."""


class GeoCRSError(GeoProcessorError):
    """Erreur liée au système de coordonnées."""


class GeoGeometryError(GeoProcessorError):
    """Erreur lors d'un traitement géométrique."""


class GeoExportError(GeoProcessorError):
    """Erreur lors de l'exportation."""
