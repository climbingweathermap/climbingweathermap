import json
import requests
from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_caching import Cache

from apscheduler.schedulers.background import BackgroundScheduler

from rich.progress import track

from .weathermap import Location

app = Flask(__name__)
app.config.from_pyfile("settings.py")
cache = Cache(app)

"""
Exampe .env

SECRET_KEY = "sectret_key"
WEATHER_KEY = "weatherapi_key"
WEATHER_API = "https://api.weatherapi.com/v1"
LOCATIONS = "./data/locations.json"

CACHE_TYPE = 'RedisCache'
CACHE_REDIS_PORT=6379
CACHE_REDIS_HOST='redis'
CACHE_REDIS_DB=0
CACHE_REDIS_URL=redis://redis:6379/0
CACHE_DEFAULT_TIMEOUT= 3600

REFRESH_MINUTES = 60

"""

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

scheduler = BackgroundScheduler()
scheduler.start()


def get_locations():
    """Get locations from open beta dataset in instance folder."""
    with open(app.config["LOCATIONS"], "r") as f:
        locations = json.load(f)

    return locations


def get_weather(locations):
    """get weather data for locations."""

    # List to hold location objects from model.py
    weather = []
    print("\n")
    for name, location in track(
        locations.items(),
        description=(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Getting"
            " Weather..."
        ),
    ):
        try:
            weather.append(
                Location(
                    name,
                    location,
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

    return weather


@scheduler.scheduled_job(
    "interval",
    id="refresh_weather",
    minutes=int(app.config["REFRESH_MINUTES"]),
)
def refresh_weather():
    """refresh the cached weather data."""
    app.logger.info(
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Getting Weather..."
    )
    weather = get_weather(get_locations())
    cache.clear()
    cache.set("weather", weather)


@app.route("/")
def root():
    return jsonify("WeatherMap")


@app.route("/api/v1/locations", methods=["GET"])
@cache.cached()
def all_locations():
    """v1 api to get location"""

    weather = cache.get("weather")

    # if weather isn't in cache then gather
    if weather is None:
        refresh_weather()
        weather = cache.get("weather")

    # jsonify everything into one response
    return jsonify([loc.to_json() for loc in weather])


# Ensure weather is gathered when initialised
refresh_weather()
