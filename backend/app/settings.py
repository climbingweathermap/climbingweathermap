"""Flask app config from enviromental variables"""

from os import environ
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = environ.get("SECRET_KEY")
print(SECRET_KEY)

WEATHER_API = environ.get("WEATHER_API")
WEATHER_KEY = environ.get("WEATHER_KEY")

LOCATIONS = environ.get("LOCATIONS")

CACHE_TYPE = environ.get("CACHE_TYPE")
CACHE_REDIS_PORT = int(environ.get("CACHE_REDIS_PORT"))  # type: ignore
CACHE_DEFAULT_TIMEOUT = int(environ.get("CACHE_DEFAULT_TIMEOUT"))  # type: ignore

CACHE_REDIS_HOST = environ.get("CACHE_REDIS_HOST")
CACHE_REDIS_URL = environ.get("CACHE_REDIS_URL")
CACHE_REDIS_DB = environ.get("CACHE_REDIS_DB")

REFRESH_MINUTES = int(environ.get("REFRESH_MINUTES"))  # type: ignore
