from app.weathermap import (
    Location,
    Weather,
    WeatherAPIError,
    WeatherNotCollectedError,
    InvalidLatLng,
)

import pytest


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
