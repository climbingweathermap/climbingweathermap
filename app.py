import json

from flask import Flask
from flask_cors import CORS

from weathermap import Location

app = Flask(__name__, instance_relative_config=True, template_folder="public")
app.config.from_pyfile("config.cfg")
"""
config.cfg example


SECRET_KEY = <"sectret_key">
WEATHER_KEY = <"weatherapi_key">
API = "https://api.weatherapi.com/v1"
LOCATIONS_PATH= <'path to locations.json'>

Locations.json example

{"Smith Rock": {"lat": 44.368, "long": -121.139}}

"""

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Get locations from open beta
# TODO

# Get locations to display weather data for
with open(app.config["LOCATIONS_PATH"], encoding="utf8") as f:
    locations = json.load(f)

# List to hold location objects from model.py
loc_objs = []
n_locs = len(locations)
for name, loc in locations.items():
    print(f"loading... {len(loc_objs)}/{n_locs} locations")
    loc_objs.append(
        Location(name, loc, app.config["API"], app.config["WEATHER_KEY"])
    )


@app.route("/")
def root():
    return f"{len(loc_objs)} locations loaded"
