""" Weathermap data models """
import requests
import json
from datetime import date, timedelta
from datetime import datetime
import pandas as pd


class Location:
    """Climbing location."""

    def __init__(self, name, data, API_URL, API_KEY):
        """Get weather data."""

        self.name = name
        self.loc = [data["lat"], data["long"]]  # list [lat,long]
        self.url = data["url"]

        # Get Weather Data

        try:
            keys = {
                "key": API_KEY,
                "q": f"{self.loc[0]},{self.loc[1]}",
                "days": 10,
            }
            self.forecast = requests.get(
                f"{API_URL}/forecast.json", params=keys
            ).json()
        except json.decoder.JSONDecodeError as e:
            raise e
        except requests.exceptions.ConnectionError as e:
            raise e

        try:
            today = date.today()

            # Previous 2 days
            dt = today - timedelta(days=2)
            dt = dt.strftime("%Y-%m-%d")
            end_dt = today.strftime("%Y-%m-%d")
            keys = {
                "key": API_KEY,
                "q": f"{self.loc[0]},{self.loc[1]}",
                "dt": dt,
                "end_dt": end_dt,
            }

            self.history = requests.get(
                f"{API_URL}/history.json", params=keys
            ).json()
        except json.decoder.JSONDecodeError as e:
            raise e
        except ConnectionError as e:
            raise e

        """Summarise weather

        Returns JSON like:
        {
            2021-07-19:
            {
                text: "Cloudy"
                icon: "//xyz.pnh"
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

        datetime_range = (
            pd.date_range(date.today(), periods=5).to_pydatetime().tolist()
        )

        date_range = [x.strftime("%Y-%m-%d") for x in datetime_range]

        self.weather = {}

        rain_score_lookup = [0.2, 0.5, 1]

        for day in date_range:
            # Select correct date from forecast api response
            for api_day in self.forecast["forecast"]["forecastday"]:
                if api_day["date"] == day:
                    day_1 = (
                        datetime.strptime(day, "%Y-%m-%d") - timedelta(days=1)
                    ).strftime("%Y-%m-%d")
                    day_2 = (
                        datetime.strptime(day, "%Y-%m-%d") - timedelta(days=2)
                    ).strftime("%Y-%m-%d")

                    rain_last_2_day = self.get_precip([day_1, day_2])

                    total_rain = (
                        api_day["day"]["totalprecip_mm"] + rain_last_2_day
                    )

                    try:
                        rain_score = list(
                            map(lambda i: i > total_rain, rain_score_lookup)
                        ).index(True)
                    except ValueError:
                        rain_score = 3  # out of limit of the lookup table

                    self.weather[day] = {
                        "text": api_day["day"]["condition"]["text"],
                        "icon": api_day["day"]["condition"]["icon"],
                        "min_temp_c": api_day["day"]["mintemp_c"],
                        "max_temp_c": api_day["day"]["maxtemp_c"],
                        "humidity": api_day["day"]["avghumidity"],
                        "rain_perc": api_day["day"]["daily_chance_of_rain"],
                        "rain_mm": api_day["day"]["totalprecip_mm"],
                        "rain_last_2_day(mm)": rain_last_2_day,
                        "rain_score": rain_score,
                    }

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