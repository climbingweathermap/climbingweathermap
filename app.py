import json
import requests

from flask import Flask, jsonify
from flask_cors import CORS


from weathermap import Location

app = Flask(__name__, instance_relative_config=True, template_folder="public")
app.config.from_pyfile("config.cfg")
"""
config.cfg example


SECRET_KEY = <"sectret_key">
WEATHER_KEY = <"weatherapi_key">
WEATHER_API = "https://api.weatherapi.com/v1"
LOCATIONS = ".\\instance\\locations.json"

"""

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get locations from open beta dataset in instance folder
with open(app.config["LOCATIONS"], "r") as f:
    sectors = json.load(f)


# List to hold location objects from model.py
loc_objs = []
n_locs = len(sectors)
for name, sector in sectors.items():
    print(f"loading... {len(loc_objs)+1}/{n_locs} sectors")
    try:
        loc_objs.append(
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


@app.route("/")
def root():
    return jsonify("WeatherMap")


@app.route("/api/v1/locations", methods=["GET"])
def all_locations():
    """v1 api to get location"""
    # jsonify everything into one response
    return jsonify([loc.to_json() for loc in loc_objs])
