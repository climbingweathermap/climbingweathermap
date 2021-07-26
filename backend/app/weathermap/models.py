""" Weathermap data models """
import requests
import json
import logging
from datetime import date, timedelta
from datetime import datetime


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
        except json.decoder.JSONDecodeError as e:
            raise e
        except requests.exceptions.ConnectionError as e:
            raise e

        """Summarise weather

        Returns JSON like:
        {
            2021-07-19:
            {
                text: "Cloudy"
                icon: "//xyz.png"
                rain_last_2_day(mm): 40
                min_temp_c:15
                max_temp_c:31
                humidity: "14"
                rain_perc: "21"
            },
            2021-07-20
            {
                ...
            }
        }

        """

        self.weather = []

        rain_score_lookup = [0.2, 0.5, 1]

        for day in self.forecast["daily"]:
            try:
                # rain is only gieven if > 0
                rain = day["rain"]
            except KeyError:
                rain = 0

            self.weather.append(
                {
                    "dt": day["dt"],
                    "text": day["weather"][0]["description"],
                    "icon": f"http://openweathermap.org/img/wn/{day['weather'][0]['icon']}@2x.png",
                    "min_temp": day["temp"]["min"],
                    "max_temp": day["temp"]["max"],
                    "temp": day["temp"]["day"],
                    "humidty": day["humidity"],
                    "rain_perc": day["pop"],
                    "rain": rain,
                    "rain_last_2_day": 0,
                    "rain_score": rain_score_lookup[0],
                }
            )

        # rain_last_2_day = self.get_precip([day_1, day_2])

        # total_rain = (
        #     api_day["day"]["totalprecip_mm"] + rain_last_2_day
        # )

        # try:
        #     rain_score = list(
        #         map(lambda i: i > total_rain, rain_score_lookup)
        #     ).index(True)
        # except ValueError:
        #     rain_score = 3  # out of limit of the lookup table

    def get_precip(self, days):
        """Get the rain fall on a given day (in mm) or list of days.

        day must be formatted as yyyy-mm-dd
        """

        # ensure its a list
        if not isinstance(days, list):
            days = [days]

        rain_mm = 0

        for day in days:
            # Select correct date from History api response
            for api_day in self.history["forecast"]["forecastday"]:
                if api_day["date"] == day:
                    rain_mm += float(api_day["day"]["totalprecip_mm"])

            # check for correct date in forecast api
            for api_day in self.forecast["forecast"]["forecastday"]:
                if api_day["date"] == day:
                    rain_mm += float(api_day["day"]["totalprecip_mm"])

        return rain_mm

    def to_json(self):
        """Return JSON version of object"""
        return {
            "name": self.name,
            "loc": self.loc,
            "weather": self.weather,
            "url": self.url,
        }
