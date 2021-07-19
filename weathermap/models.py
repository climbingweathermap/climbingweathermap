""" Weathermap data models """
import requests
from datetime import date, timedelta


class Location:
    """Climbing location."""

    def __init__(self, data, API_URL, API_KEY):
        """Get weather data."""

        self.name = data["meta_parent_sector"]
        self.loc = [data["lat"], data["lng"]]  # list [lat,long]
        self.nroutes = data["count"]

        # Get Weather Data
        keys = {"key": API_KEY, "q": f"{self.loc[0]},{self.loc[1]}"}
        self.current = requests.get(
            f"{API_URL}/current.json", params=keys
        ).json()

        keys = {
            "key": API_KEY,
            "q": f"{self.loc[0]},{self.loc[1]}",
            "days": 10,
        }
        self.forecast = requests.get(
            f"{API_URL}/forecast.json", params=keys
        ).json()

        # today = date.today()

    # # 3 days so then can extract last 48 hours
    # dt = today - timedelta(days=3)
    # dt = dt.strftime("%Y-%m-%d")
    # end_dt = today.strftime("%Y-%m-%d")
    # keys = {
    #     "key": API_KEY,
    #     "q": f"{self.loc[0]},{self.loc[1]}",
    #     "dt": dt,
    #     "end_dt": end_dt,
    # }
    # self.history = requests.get(
    #     f"{API_URL}/history.json", params=keys
    # ).json()

    def weather_summary(self):
        """Summarise weather"""
        return "Weather is good"

    def to_json(self):
        """Return JSON version of object"""
        return {
            "name": self.name,
            "loc": self.loc,
            "weather": self.weather_summary(),
            "count": self.nroutes,
        }
