import json
import requests

from flask import Flask, jsonify
from flask_cors import CORS
from flask_caching import Cache


from weathermap import Location

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.cfg")
cache = Cache(app)

"""
config.cfg example


SECRET_KEY = <"sectret_key">
WEATHER_KEY = <"weatherapi_key">
WEATHER_API = "https://api.weatherapi.com/v1"
LOCATIONS = ".\\instance\\locations.json"

"""

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_locations():
    """Get locations from open beta dataset in instance folder."""
    with open(app.config["LOCATIONS"], "r") as f:
        locations = json.load(f)

    return locations


def get_weather(sectors):
    """get weather data for sectors."""

    # List to hold location objects from model.py
    locations = []
    n_locs = len(sectors)
    for name, sector in sectors.items():
        print(f"loading... {len(locations)+1}/{n_locs} locations")
        try:
            locations.append(
                Location(
                    name,
                    sector,
                    app.config["WEATHER_API"],
                    app.config["WEATHER_KEY"],
                )
            )
        except json.decoder.JSONDecodeError as e:
            print(e)
            print(f"failed = {name}")
        except requests.exceptions.ConnectionError as e:
            print(e)
            print(f"failed = {name}")

    return locations


@app.route("/")
def root():
    return jsonify("WeatherMap")


@app.route("/api/v1/locations", methods=["GET"])
@cache.cached()
def all_locations():
    """v1 api to get location"""
    locations = get_locations()
    weather = get_weather(locations)

    # jsonify everything into one response
    return jsonify([loc.to_json() for loc in weather])


if __name__ == "__main__":
    app.run()
