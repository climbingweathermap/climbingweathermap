from os import environ


SECRET_KEY = environ.get("SECRET_KEY")
WEATHER_API = environ.get("WEATHER_API")
WEATHER_KEY = environ.get("WEATHER_KEY")
LOCATIONS = environ.get("LOCATIONS")
CACHE_DEFAULT_TIMEOUT = environ.get("CACHE_DEFAULT_TIMEOUT")
CACHE_TYPE = environ.get("CACHE_TYPE")
REFRESH_MINUTES = environ.get("REFRESH_MINUTES")
