# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=eucs_platform.settings.production
from .base import *  # NOQA
import logging.config

# For security and performance reasons, DEBUG is turned off
DEBUG = False
TEMPLATE_DEBUG = False

# Strict password authentication and validation
# To use this setting, install the Argon2 password hashing algorithm.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

CSRF_TRUSTED_ORIGINS = ["http://localhost", "https://citizen-science-nl.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Must mention ALLOWED_HOSTS in production!
# ALLOWED_HOSTS = ["eucs_platform.com"]

# Cache the templates in memory for speed-up
loaders = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

TEMPLATES[0]["OPTIONS"].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})

# Define STATIC_ROOT for the collectstatic command
STATIC_ROOT = str(BASE_DIR.parent / "site" / "static")

# Log everything to the logs directory at the top
LOGFILE_ROOT = BASE_DIR.parent / "logs"

# Reset logging
LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "proj_log_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(LOGFILE_ROOT / "project.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {"project": {"handlers": ["proj_log_file"], "level": "DEBUG"}},
}

logging.config.dictConfig(LOGGING)
