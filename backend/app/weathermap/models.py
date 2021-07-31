""" Weathermap data models """
import json
from datetime import datetime, timedelta

import requests


class Location:
    """Climbing location."""

    def __init__(self, ref, data):
        """Climbing Location."""
        # Check lat and long are valid

        try:
            # list [lat,long]
            self.latlng = [float(data["lat"]), float(data["long"])]
        except ValueError:
            # Invalid input so raise latlng error
            raise InvalidLatLng([data["lat"], data["long"]])

        if (-90 < self.latlng[0] < 90) and (-180 < self.latlng[1] < 180):
            self.ref = ref
            self.name = data["name"]
            self.url = data["url"]
        else:
            raise InvalidLatLng(self.latlng)

    def to_dict(self):
        """Return dict version of object"""
        return self.__dict__


class Weather:
    """Weather current and forecast at a single location"""

    def __init__(self, location, api_url, api_key, get_weather=False):
        """Initialise."""

        self.location = location

        self.api_url = api_url
        self.api_key = api_key

        self.history = None
        self.forecast = None
        self.weather = None

        if get_weather:
            self.get_weather()
            self.summarise_weather()

    def get_forecast(self):
        """Get forecast weather"""

        # Current and Forecast
        try:
            keys = {
                "lat": self.location.latlng[0],
                "lon": self.location.latlng[1],
                "appid": self.api_key,
                "exclude": "minutely,hourly,alerts,current",
                "units": "metric",
            }
            self.forecast = requests.get(self.api_url, params=keys).json()
        except (
            json.decoder.JSONDecodeError,
            requests.exceptions.ConnectionError,
            KeyError,
        ) as error:
            raise WeatherAPIError(error) from error

        # Empty results list returns error
        if not self.forecast:
            raise WeatherAPIError("Empty Response")

    def get_history(self):
        """Get historical weather data."""
        if not self.forecast:
            raise WeatherAPIError(
                "get_forecast() must be called before get_history()"
            )

        try:

            today = datetime.fromtimestamp(self.forecast["daily"][0]["dt"])

            dt = round(datetime.timestamp(today - timedelta(days=3)))

            keys = {
                "lat": self.location.latlng[0],
                "lon": self.location.latlng[1],
                "appid": self.api_key,
                "units": "metric",
                "dt": dt,
            }

            self.history = requests.get(
                f"{self.api_url}/timemachine", params=keys
            ).json()

        except (
            json.decoder.JSONDecodeError,
            requests.exceptions.ConnectionError,
            KeyError,
        ) as error:
            raise WeatherAPIError(error) from error

        # Empty results list returns error
        if not self.history:
            raise WeatherAPIError("Empty Response")

    def get_weather(self):
        """Retrieve historical and forecast weather
        from API for a single lcoation."""

        try:
            self.get_forecast()
            self.get_history()
        except WeatherAPIError as error:
            raise error

    def summarise_weather(self):
        """Summarise weather."""

        if self.history is None or self.forecast is None:
            raise WeatherNotCollectedError

        self.weather = []

        rain_score_lookup = [0.1, 0.4, 1]

        for day in self.forecast["daily"]:
            try:
                # rain is only given if rain > 0
                rain = day["rain"]
            except KeyError:
                rain = 0

            dt = day["dt"]
            start_dt = round(
                datetime.timestamp(
                    datetime.fromtimestamp(dt) - timedelta(days=2)
                )
            )

            rain_last_2_day = self.get_precip([start_dt, dt])  # noqa

            total_rain = rain + rain_last_2_day

            try:
                rain_score = list(
                    map(lambda i: i > total_rain, rain_score_lookup)
                ).index(True)
            except ValueError:
                rain_score = 3  # out of limit of the lookup table

            icon = (
                "https://openweathermap.org/img/wn/"
                f"{day['weather'][0]['icon']}@2x.png"
            )
            self.weather.append(
                {
                    "dt": dt,
                    "text": day["weather"][0]["description"],
                    "icon": icon,
                    "min_temp": day["temp"]["min"],
                    "max_temp": day["temp"]["max"],
                    "temp": day["temp"]["day"],
                    "humidity": day["humidity"],
                    "rain_perc": round(100 * day["pop"], 1),
                    "rain": round(rain, 1),
                    "rain_last_2_day": rain_last_2_day,
                    "rain_score": rain_score,
                }
            )

    def get_precip(self, dt_range):
        """Get the rain fall during a given range of dt.

        [start_dt, end_dt]

        """

        if self.history is None or self.forecast is None:
            raise WeatherNotCollectedError

        # ensure list is sorted correctly
        dt_range.sort()

        rain = 0

        # start with history
        for hour in self.history["hourly"]:
            if dt_range[0] < hour["dt"] < dt_range[1]:
                try:
                    rain += Weather.sum_all_rain(hour["rain"])
                except KeyError:
                    # No rain in the period
                    pass

        # Use forecast
        for day in self.forecast["daily"]:
            if dt_range[0] < day["dt"] < dt_range[1]:
                try:
                    rain += Weather.sum_all_rain(day["rain"])
                except KeyError:
                    # No rain in the period
                    pass

        return rain

    def to_dict(self):
        """Return dict version of object"""

        return {"weather": self.weather, "location": self.location.to_dict()}

    @staticmethod
    def sum_all_rain(rain):
        """Sums up all rain in the response dict from the api call"""
        # Handle if a dict or a value
        if isinstance(rain, dict):
            total_rain = 0
            for item in rain.values():
                total_rain += float(item)
        else:
            total_rain = float(rain)

        return total_rain


class WeatherAPIError(Exception):
    """Raised when weather api returns and invalid result"""

    def __init__(self, source):
        self.source = source
        super().__init__(source)

    def __str__(self):
        return f"Source of error: {self.source}"


class WeatherNotCollectedError(Exception):
    """Raised when weather data is needed but not collected"""

    def __str__(self):
        return "Weather must be collected from the API first"


class InvalidLatLng(Exception):
    """Lat Long coords are not valid."""

    def __init__(self, latlng):
        self.latlng = latlng
        super().__init__(latlng)

    def __str__(self):
        return f"Invalid Coordinates, lat/long = {self.latlng}"
