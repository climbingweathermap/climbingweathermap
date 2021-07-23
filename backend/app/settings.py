from os import environ
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = environ.get("SECRET_KEY")
WEATHER_API = environ.get("WEATHER_API")
WEATHER_KEY = environ.get("WEATHER_KEY")
LOCATIONS = environ.get("LOCATIONS")
CACHE_TYPE = environ.get("CACHE_TYPE")
CACHE_DEFAULT_TIMEOUT = int(environ.get("CACHE_DEFAULT_TIMEOUT"))
REFRESH_MINUTES = int(environ.get("REFRESH_MINUTES"))
