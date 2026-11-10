import pytest
from pydantic import ValidationError

from geoprocessor.schemas import BufferRequest


def test_valid_buffer_config():

    config = BufferRequest(distance=100.0, target_epsg=2950)

    assert config.distance == 100.0
    assert config.target_epsg == 2950


def test_negative_distance():

    with pytest.raises(ValidationError):
        BufferRequest(distance=-50.0, target_epsg=2950)


def test_invalid_epsg():

    with pytest.raises(ValidationError):
        BufferRequest(distance=100.0, target_epsg=-1)


def test_invalid_distance_type():

    with pytest.raises(ValidationError):
        BufferRequest(distance="cent mètres", target_epsg=2950)


def test_infinite_distance():

    with pytest.raises(ValidationError):
        BufferRequest(distance=float("inf"), target_epsg=2950)
