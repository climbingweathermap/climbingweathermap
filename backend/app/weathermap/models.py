""" Weathermap data models """
import requests
import json
from datetime import datetime, timedelta


class Location:
    """Climbing location."""

    def __init__(self, name, data, API_URL, API_KEY):
        """Get weather data."""

        self.name = name
        self.loc = [data["lat"], data["long"]]  # list [lat,long]
        self.url = data["url"]

        # Get Weather Data
        # https://openweathermap.org/api/one-call-api

        try:
            keys = {
                "lat": self.loc[0],
                "lon": self.loc[1],
                "appid": API_KEY,
                "exclude": "minutely,hourly,alerts,current",
                "units": "metric",
            }
            self.forecast = requests.get(API_URL, params=keys).json()

            keys = {
                "lat": self.loc[0],
                "lon": self.loc[1],
                "appid": API_KEY,
                "units": "metric",
                "dt": round(
                    datetime.timestamp(
                        datetime.fromtimestamp(self.forecast["daily"][0]["dt"])
                        - timedelta(days=2)
                    )
                ),
            }
            self.history = requests.get(
                f"{API_URL}/timemachine", params=keys
            ).json()

        except json.decoder.JSONDecodeError as e:
            raise e
        except requests.exceptions.ConnectionError as e:
            raise e

        """Summarise weather

        Returns JSON like:
        [
            1627156800:
            {
                dt: 1627156800
                text: "Cloudy"
                icon: "//xyz.png"
                rain: 0.5
                rain_last_2_day: 10.2
                min_temp:15
                max_temp:31
                humidity: "14"
                rain_perc: "21"
            },
            {
                ...
            }
        ]

        """

        self.weather = []

        rain_score_lookup = [0.1, 0.4, 1]

        for day in self.forecast["daily"]:
            try:
                # rain is only gieven if > 0
                rain = day["rain"]
            except KeyError:
                rain = 0

            dt = day["dt"]
            start_dt = round(
                datetime.timestamp(
                    datetime.fromtimestamp(dt) - timedelta(days=2)
                )
            )

            rain_last_2_day = self.get_precip([start_dt, dt])

            total_rain = rain + rain_last_2_day

            try:
                rain_score = list(
                    map(lambda i: i > total_rain, rain_score_lookup)
                ).index(True)
            except ValueError:
                rain_score = 3  # out of limit of the lookup table

            self.weather.append(
                {
                    "dt": dt,
                    "text": day["weather"][0]["description"],
                    "icon": f"https://openweathermap.org/img/wn/{day['weather'][0]['icon']}@2x.png",
                    "min_temp": day["temp"]["min"],
                    "max_temp": day["temp"]["max"],
                    "temp": day["temp"]["day"],
                    "humidity": day["humidity"],
                    "rain_perc": 100 * day["pop"],
                    "rain": rain,
                    "rain_last_2_day": rain_last_2_day,
                    "rain_score": rain_score,
                }
            )

    def get_precip(self, dt_range):
        """Get the rain fall during a given range of dt.

        [start_dt, end_dt]

        """

        rain = 0

        # start with history
        for hour in self.history["hourly"]:
            if dt_range[0] < hour["dt"] < dt_range[1]:
                try:
                    rain += Location.sum_all_rain(hour["rain"])
                except KeyError:
                    # No rain in the period
                    pass

        # Use forecast
        for day in self.forecast["daily"]:
            if dt_range[0] < day["dt"] < dt_range[1]:
                try:
                    rain += Location.sum_all_rain(day["rain"])
                except KeyError:
                    # No rain in the period
                    pass

        return rain

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

    def to_json(self):
        """Return JSON version of object"""
        return {
            "name": self.name,
            "loc": self.loc,
            "weather": self.weather,
            "url": self.url,
        }
