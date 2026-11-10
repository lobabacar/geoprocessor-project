import pytest

from geoprocessor.exceptions import (
    GeoCRSError,
    GeoDataLoadError,
    GeoProcessorError,
)
from geoprocessor.processor import GeoProcessor


def test_missing_file(tmp_path):
    """Vérifie l'erreur de chargement."""

    processor = GeoProcessor(tmp_path / "inexistant.gpkg")

    with pytest.raises(GeoDataLoadError):
        processor.load()


def test_reprojection_without_load(tmp_path):
    """Vérifie l'état avant chargement."""

    processor = GeoProcessor(tmp_path / "zones.gpkg")

    with pytest.raises(RuntimeError):
        processor.reproject(2950)


def test_exception_inheritance():
    """Vérifie l'héritage des exceptions."""

    assert issubclass(
        GeoDataLoadError,
        GeoProcessorError,
    )

    assert issubclass(
        GeoCRSError,
        GeoProcessorError,
    )
