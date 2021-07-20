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
LOCATIONS_API= "https://climb-api.openbeta.io/geocode/v1/sectors"

"""

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get locations from open beta
query = {"latlng": "45.482300,-122.558441", "radius": 100}
sectors = requests.get(
    app.config["LOCATIONS_API"], params=query, verify=False
).json()

# List to hold location objects from model.py
loc_objs = []
n_locs = len(sectors)
for sector in sectors:
    print(f"loading... {len(loc_objs)+1}/{n_locs} sectors")
    loc_objs.append(
        Location(sector, app.config["WEATHER_API"], app.config["WEATHER_KEY"])
    )


@app.route("/")
def root():
    return jsonify("WeatherMap")


@app.route("/api/v1/locations", methods=["GET"])
def all_locations():
    """v1 api to get location"""
    # jsonify everything into one response
    return jsonify([loc.to_json() for loc in loc_objs])
