"""App backend pytest suite"""

from app.weathermap import (
    Location,
    Weather,
    WeatherAPIError,
    WeatherNotCollectedError,
    InvalidLatLng,
)

import pytest
import requests


class Mock_Forecast:
    @staticmethod
    def json():
        return {"forecast": 1}


class Mock_History:
    @staticmethod
    def json():
        return {"history": 1}


def mock_get(url, params=None):
    if "timemachine" in url:
        return Mock_Forecast()
    else:
        return Mock_History()


@pytest.fixture
def my_location():
    """Sample location object for testing."""

    data = {
        "name": "good location",
        "url": "https://openweathermap.org/api/one-call-api",
        "lat": 33.44,
        "long": -94.04,
    }
    return Location(1, data)


@pytest.fixture
def my_weather_nocall(my_location):
    """Sample weather object for testing."""
    return Weather(my_location, "APIURL", "APIKEY")


@pytest.fixture
def my_weather(my_location, monkeypatch):
    """Sample weather object for testing."""
    monkeypatch.setattr(requests, "get", mock_get)
    return Weather(my_location, "APIURL", "APIKEY", get_weather=True)


@pytest.mark.parametrize(
    "latlng", [[95, 0], [-95, 0], [0, 190], [0, -190], ["abc", 0], [0, "abc"]]
)
def test_invalid_latlng(latlng):
    """Test weather invalid latlng coords are raising
    an error on object creation."""

    data = {
        "name": "bad location",
        "url": "https://openweathermap.org/api/one-call-api",
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
        "url": "https://openweathermap.org/api/one-call-api",
        "latlng": [33.44, -94.04],
    }


def test_weather_to_dict_nocall(my_location, my_weather_nocall):
    """Test creating a weather object (without an API call) and return dict."""
    assert my_weather_nocall.to_dict() == {
        "weather": None,
        "location": my_location.to_dict(),
    }


def test_weather_to_dict_withcall(my_location, my_weather):
    """Test creating a weather object and return dict."""
    assert my_weather.to_dict() == {
        "weather": "some stuff",
        "location": my_location.to_dict(),
    }


def test_get_weather(my_weather):
    """Test weather api call using mock"""
