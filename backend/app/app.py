"""App for climbing weather map (flask backend)."""

import json
import logging
from datetime import datetime

from flask import Flask, jsonify, Response
from flask.logging import create_logger
from flask_cors import CORS
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from rich.progress import track

from .weathermap import Location, Weather, WeatherAPIError

app = Flask(__name__)
app.config.from_pyfile("settings.py")
cache = Cache(app)
logger = create_logger(app)

"""
Exampe .env

SECRET_KEY = "sectret_key"
WEATHER_KEY = "weatherapi_key"
WEATHER_API = "https://api.openweathermap.org/data/2.5/onecall"
LOCATIONS = "./data/locations.json"

CACHE_TYPE = 'RedisCache'
CACHE_REDIS_PORT=6379
CACHE_REDIS_HOST='redis'
CACHE_REDIS_DB=0
CACHE_REDIS_URL=redis://redis:6379/0
CACHE_DEFAULT_TIMEOUT= 0

REFRESH_MINUTES = 360

"""

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

scheduler = BackgroundScheduler()
scheduler.start()


@cache.cached(key_prefix="location", timeout=300)
def get_locations(path_to_locations):
    """Get locations from local dataset"""

    with open(path_to_locations, "r") as json_file:
        location_list = json.load(json_file)

    locations = [Location(i, location_list[i]) for i in location_list]
    logger.info("Locations read")

    return locations


def get_weather(locations):
    """get weather data for locations."""

    weather = []
    for location in track(
        locations,
        description=(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Getting"
            " Weather..."
        ),
    ):
        try:
            weather.append(
                Weather(
                    location,
                    app.config["WEATHER_API"],
                    app.config["WEATHER_KEY"],
                    get_weather=True,
                )
            )
        except WeatherAPIError as e:
            logger.error(e)
            logger.error(f"Weather API error, failed = {location.name}")

    return weather


@scheduler.scheduled_job(
    "interval",
    id="refresh_weather",
    minutes=int(app.config["REFRESH_MINUTES"]),
)
def refresh_weather():
    """refresh the cached weather data."""
    logger.info("Getting Weather...")
    locations = get_locations(app.config["LOCATIONS"])
    weather = get_weather(locations)
    # Check that at least some weather was gathered.
    if weather:
        logger.info("Weather Collected")
        cache.set("weather", weather)
    else:
        logger.error("Weather could not be gathered")


@app.route("/api/v1/locations", methods=["GET"])
def all_locations():
    """v1 api to get location using cache"""

    locations = get_locations(app.config["LOCATIONS"])

    # jsonify everything into one response
    response = jsonify([loc.to_dict() for loc in locations])

    return response


@app.route("/api/v1/weather", methods=["GET"])
def all_weather():
    """v1 api to get location and weather using cache"""

    weather = cache.get("weather")

    # if weather isn't in cache then return error code
    if weather is None:
        return Response(
            response="Weather Data not available in Cache", status=500
        )

    # jsonify everything into one response
    response = jsonify([loc.to_dict() for loc in weather])

    return response


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
    cache.clear()
    refresh_weather()
