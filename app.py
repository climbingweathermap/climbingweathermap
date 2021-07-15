from flask import Flask
import requests

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.cfg")

aqi = "no"
q = "London"

print(app.config["API"])
request_str = f"{app.config['API']}/current.json"
keys = {"key": app.config["WEATHER_KEY"], "q": q, "aqi": aqi}

r = requests.get(request_str, params=keys)

print(r.url)
print(r)
print("-------------------------------------")
print(r.json())


@app.route("/")
def boonjour():
    return r.json()
