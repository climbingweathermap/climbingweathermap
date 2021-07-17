import json

from flask import Flask, render_template, url_for, redirect
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
CORS(app, resources={r"/index/*": {"origins": "*"}})

# Get locations for open beta

df = pd.read_json(
    "../../opendata/openbeta-usa-routes-aug-2020.zip", lines=True
)
print(df)

# Get locations to display weather data for
with open(app.config["LOCATIONS_PATH"]) as f:
    locations = json.load(f)

# List to hold location objects from model.py
loc_objs = []
for name, loc in locations.items():
    loc_objs.append(
        Location(name, loc, app.config["API"], app.config["WEATHER_KEY"])
    )


@app.route("/")
def root():
    return render_template("index.html")
