import json

from flask import Flask

from weathermap import Location

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.cfg")
"""
SECRET_KEY = <"sectret_key">
WEATHER_KEY = <"weatherapi_key">
API = "https://api.weatherapi.com/v1"
LOCATIONS_PATH= <'path to locations.json'>


"""

# Get locations to display weather data for
with open(app.config["LOCATIONS_PATH"]) as f:
    locations = json.load(f)

# List oto hold location objects from model.py
loc_objs = []
for name, loc in locations.items():
    loc_objs.append(
        Location(name, loc, app.config["API"], app.config["WEATHER_KEY"])
    )


@app.route("/")
def boonjour():
    return str(len(loc_objs))
