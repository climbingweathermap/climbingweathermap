""" Weathermap data models """
import requests
from datetime import date, timedelta


class Location:
    """Climbing location."""

    def __init__(self, name, loc, API_URL, API_KEY):
        """Get weather data."""

        keys = {"key": API_KEY, "q": f"{loc['lat']},{loc['long']}"}
        self.current = requests.get(
            f"{API_URL}/current.json", params=keys
        ).json()

        keys = {"key": API_KEY, "q": f"{loc['lat']},{loc['long']}", "days": 10}
        self.forecast = requests.get(
            f"{API_URL}/forecast.json", params=keys
        ).json()

        today = date.today()

        # 3 days so then can extract last 48 hours
        dt = today - timedelta(days=3)
        dt = dt.strftime("%Y-%m-%d")

        end_dt = today.strftime("%Y-%m-%d")

        keys = {
            "key": API_KEY,
            "q": f"{loc['lat']},{loc['long']}",
            "dt": dt,
            "end_dt": end_dt,
        }
        self.history = requests.get(
            f"{API_URL}/history.json", params=keys
        ).json()
