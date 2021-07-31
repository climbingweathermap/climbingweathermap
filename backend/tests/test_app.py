"""App backend pytest suite"""

from app.weathermap import (
    Location,
    Weather,
    WeatherAPIError,
    WeatherNotCollectedError,
    InvalidLatLng,
)

import pytest


@pytest.fixture
def my_location():
    """Sample location object for testing."""

    data = {
        "name": "good location",
        "url": "www.google.com",
        "lat": 45.002,
        "long": -122.562,
    }
    return Location(1, data)


@pytest.fixture
def my_weather(my_location):
    """Sample weather object for testing."""
    return Weather(my_location, "abc", "def")


@pytest.mark.parametrize(
    "latlng", [[95, 0], [-95, 0], [0, 190], [0, -190], ["abc", 0], [0, "abc"]]
)
def test_invalid_latlng(latlng):
    """Test weather invalid latlng coords are raising
    an error on object creation."""

    data = {
        "name": "bad location",
        "url": "www.google.com",
        "lat": latlng[0],
        "long": latlng[1],
    }
    with pytest.raises(InvalidLatLng):
        Location(1, data)


def test_location_to_dict(my_location):
    """Test creating a location object and returning a dictionary."""
    assert my_location.to_dict() == {
        "ref": 1,
        "name": "good location",
        "url": "www.google.com",
        "latlng": [45.002, -122.562],
    }


def test_weather_to_dict(my_location, my_weather):
    """Test creating a weather object and return dict."""
    assert my_weather.to_dict() == {
        "weather": None,
        "location": my_location.to_dict(),
    }
