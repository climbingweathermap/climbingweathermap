"""App for climbing weather map (flask backend)."""

import json
import logging
from flask import Flask, jsonify, Response
from flask.logging import create_logger
from flask_cors import CORS  # type: ignore
from flask_caching import Cache  # type: ignore
from apscheduler.schedulers.background import (  # type: ignore
    BackgroundScheduler,  # type: ignore
)

from .weathermap import Location, WeatherAPIError


app = Flask(__name__)
app.config.from_pyfile("settings.py")
cache = Cache(app)
logger = create_logger(app)

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

scheduler = BackgroundScheduler()
scheduler.start()


@cache.cached(timeout=300)
def get_locations(path_to_locations: str) -> list[Location]:
    """Get locations from local dataset"""

    with open(path_to_locations, "r") as json_file:
        location_json = json.load(json_file)

    locations: list[Location] = Location.create_location_tree(location_json)
    logger.info("Locations read from source")

    return locations


@scheduler.scheduled_job(
    "interval",
    id="refresh_weather",
    minutes=int(app.config["REFRESH_MINUTES"]),
)
def refresh_weather():
    """refresh the cached weather data."""
    logger.info("Getting Weather...")
    locations: list[Location] = get_locations(app.config["LOCATIONS"])
    for loc in locations:
        try:
            loc.get_weather(
                app.config["WEATHER_API"], app.config["WEATHER_KEY"]
            )

        except WeatherAPIError as error:
            logger.error(error)
            logger.error(f"Weather API error, failed = {loc.name}")

    logger.info("Weather Collected")
    cache.set("locations", locations)


@app.route("/api/v1/locations", methods=["GET"])
def all_locations() -> Response:
    """v1 api to get location using cache"""
    locations = cache.get("locations")

    # if weather isn't in cache then return error code
    if locations is None:
        return Response(
            response="Weather/Lcoation Data not available in Cache", status=500
        )

    # jsonify everything into one response
    response: Response = jsonify([loc.to_dict() for loc in locations])

    return response


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
    cache.clear()
    refresh_weather()
