""" Weathermap data models """
import requests
from datetime import date, timedelta
import pandas as pd


class Location:
    """Climbing location."""

    def __init__(self, data, API_URL, API_KEY):
        """Get weather data."""

        self.name = data["meta_parent_sector"]
        self.loc = [data["lat"], data["lng"]]  # list [lat,long]
        self.nroutes = data["count"]

        # Get Weather Data
        keys = {
            "key": API_KEY,
            "q": f"{self.loc[0]},{self.loc[1]}",
            "days": 10,
        }
        self.forecast = requests.get(
            f"{API_URL}/forecast.json", params=keys
        ).json()

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

    def weather_summary(self):
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
                humidity: "14%"
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

        response = {}

        for day in date_range:
            # Select correct date from forecast api response
            for api_day in self.forecast["forecast"]["forecastday"]:
                if api_day["date"] == day:

                    response[day] = {
                        "text": api_day["day"]["condition"]["text"],
                        "icon": api_day["day"]["condition"]["icon"],
                    }

        print(response)
        return response

    def to_json(self):
        """Return JSON version of object"""
        return {
            "name": self.name,
            "loc": self.loc,
            "weather": self.weather_summary(),
            "count": self.nroutes,
        }
