from decouple import config
from .base import *  # NOQA


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_URL"),
    }
}

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")


SIMPLE_JWT.update(
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60 * 24),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    }
)
