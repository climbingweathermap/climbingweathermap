"""App for climbing weather map (flask backend)."""

import json
import logging
from flask import Flask, jsonify, Response, request
from flask_cors import CORS  # type: ignore
from flask_caching import Cache  # type: ignore
from apscheduler.schedulers.background import (  # type: ignore
    BackgroundScheduler,  # type: ignore
)

from .weathermap import Location, WeatherAPIError


app = Flask(__name__)
app.config.from_pyfile("settings.py")
cache = Cache(app)

log = logging.getLogger(__name__)

# Configure Logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

scheduler = BackgroundScheduler()
scheduler.start()


def get_locations(path_to_locations: str) -> list[Location]:
    """Get locations from local dataset"""

    with open(path_to_locations, "r") as json_file:
        location_json = json.load(json_file)

    locations: list[Location] = Location.create_location_tree(location_json)
    log.info("Locations read from source")

    return locations


@scheduler.scheduled_job(
    "interval",
    id="refresh_weather",
    minutes=int(app.config["REFRESH_MINUTES"]),
)
def refresh_weather():
    """refresh the cached weather data."""
    log.info("Getting Weather...")
    locations: list[Location] = get_locations(app.config["LOCATIONS"])
    log.debug(locations)
    for loc in locations:
        try:
            loc.get_weather(app.config["WEATHER_API"], app.config["WEATHER_KEY"])

        except WeatherAPIError as error:
            log.error(error)
            log.error(f"Weather API error, failed = {loc.name}")

    log.info("Weather Collected")

    cache.set("locations", locations)

    # log cache keys after getting weather
    log.debug("Locations fetched")


@app.route("/api/v1/locations", methods=["GET"])
def all_locations() -> Response:
    """v1 api to get location from cache.
    drill param is used to specify how many levels
    to drill into location tree"""
    locations: list[Location] = cache.get("locations")
    log.debug("Locations:")
    log.debug(locations)
    # if weather isn't in cache then return error code
    if locations is None:
        return Response(
            response="Weather/Location Data not available in Cache", status=500
        )

    # drill down
    if "drill" in request.args:
        try:
            drill = int(request.args["drill"])
            for _ in range(drill):
                locations = Location.drill(locations)
        except ValueError:
            return Response(
                response=(
                    "Invalid aprameter passed for drill, must be int:"
                    f" {request.args['drill']} was provided"
                ),
                status=500,
            )

    # jsonify everything into one response
    return jsonify([loc.to_dict() for loc in locations])


if __name__ != "__main__":
    cache.clear()
    refresh_weather()
