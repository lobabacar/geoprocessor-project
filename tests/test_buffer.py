import pytest

from geoprocessor.processor import GeoProcessor


@pytest.mark.parametrize(
    "distance",
    [
        -1,
        -10,
        float("nan"),
        float("inf"),
        True,
        "100",
    ],
)
def test_invalid_buffer_distance(distance, sample_points):

    processor = GeoProcessor("data/points.gpkg")

    processor.gdf = sample_points

    with pytest.raises(ValueError):
        processor.buffer(distance)


@pytest.mark.parametrize(
    "distance",
    [0, 10, 50, 100],
)
def test_valid_buffer_distance(distance, sample_points):

    processor = GeoProcessor("data/points.gpkg")

    processor.gdf = sample_points

    processor.buffer(distance)

    assert len(processor.gdf) == 3

    assert processor.gdf.geometry.is_valid.all()
