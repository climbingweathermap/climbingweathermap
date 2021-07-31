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
        return {
            "lat": 33.44,
            "lon": -94.04,
            "timezone": "America/Chicago",
            "timezone_offset": -21600,
            "daily": [
                {
                    "dt": 1618308000,
                    "sunrise": 1618282134,
                    "sunset": 1618333901,
                    "moonrise": 1618284960,
                    "moonset": 1618339740,
                    "moon_phase": 0.04,
                    "temp": {
                        "day": 15,
                        "min": 5.09,
                        "max": 24.07,
                        "night": 5.09,
                        "eve": 9.21,
                        "morn": 8.49,
                    },
                    "feels_like": {
                        "day": 17.59,
                        "night": 6.27,
                        "eve": 6.49,
                        "morn": 6.27,
                    },
                    "pressure": 1020,
                    "humidity": 81,
                    "dew_point": 6.77,
                    "wind_speed": 3.06,
                    "wind_deg": 294,
                    "weather": [
                        {
                            "id": 500,
                            "main": "Rain",
                            "description": "light rain",
                            "icon": "10d",
                        }
                    ],
                    "clouds": 56,
                    "pop": 0.2,
                    "rain": 0.62,
                    "uvi": 1.93,
                }
            ],
        }


class Mock_History:
    @staticmethod
    def json():
        return {
            "lat": 33.44,
            "lon": -94.04,
            "timezone": "America/Chicago",
            "timezone_offset": -21600,
            "hourly": [
                {
                    "dt": 1586390400,
                    "temp": 8.41,
                    "feels_like": 1.43,
                    "pressure": 1006,
                    "humidity": 65,
                    "dew_point": 2.46,
                    "clouds": 0,
                    "wind_speed": 9.83,
                    "wind_deg": 60,
                    "wind_gust": 15.65,
                    "weather": [
                        {
                            "id": 800,
                            "main": "Clear",
                            "description": "clear sky",
                            "icon": "01n",
                        }
                    ],
                }
            ],
        }


def mock_get(url, params=None):
    if "timemachine" in url:
        return Mock_History()
    else:
        return Mock_Forecast()


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
        "weather": my_weather.weather,
        "location": my_location.to_dict(),
    }


def test_get_precip_error(my_weather_nocall):
    """test weather get precip raises an error if
    weather data is not collected first."""
    with pytest.raises(WeatherNotCollectedError):
        my_weather_nocall.get_precip([1627599277, 1627772077])


def test_get_precip(my_weather):
    pass


def test_summarise_no_weather(my_weather_nocall):
    """Test when summarise weather is called
    before any is collected from API."""
    with pytest.raises(WeatherNotCollectedError):
        my_weather_nocall.summarise_weather()


def test_summarise_weather(my_weather):
    """Test that summarise weather behaves as expected."""
    expected_summary = [
        {
            "dt": 1618308000,
            "text": "light rain",
            "icon": "https://openweathermap.org/img/wn/10d@2x.png",
            "rain": 0.6,
            "rain_last_2_day": 0,
            "temp": 15,
            "min_temp": 5.09,
            "rain_perc": 20,
            "max_temp": 24.07,
            "humidity": 81,
            "rain_score": 2,
        }
    ]

    assert my_weather.weather == expected_summary


@pytest.mark.parametrize(
    "rain,total", [({"1h": 5, "2h": "3", "3h": 2}, 10), ("2", 2)]
)
def test_sum_all_rain(rain, total):
    """Test sum all rain static method."""
    assert Weather.sum_all_rain(rain) == total


def test_WeatherAPIError_response():
    """Check string output of WeatherAPIError."""
    response_str = "Source of error: unknown"
    assert str(WeatherAPIError("unknown")) == response_str


def test_WeatherNotCollectedError_response():
    """Check string output of WeatherNotCollectedError."""
    response_str = "Weather must be collected from the API first"
    assert str(WeatherNotCollectedError()) == response_str


def test_InvalidLatLng_response():
    """Check string output of InvalidLatLng."""
    response_str = "Invalid Coordinates, lat/long = [45, -129]"
    assert str(InvalidLatLng([45, -129])) == response_str
