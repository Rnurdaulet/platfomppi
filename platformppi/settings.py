import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "!!!REPLACE_ME_IN_PROD!!!")

DEBUG = os.getenv("DEBUG", "0") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Apps
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "whitenoise",
    "dal",
    "dal_select2",
    "django_select2",

    "apps.accounts",
    "apps.lookups",
    "apps.contest",
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Auth
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/login/ecp/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ROOT_URLCONF = "platformppi.urls"
WSGI_APPLICATION = "platformppi.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
USE_SQLITE = os.getenv("USE_SQLITE", "1") == "1"

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Aqtobe"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("ru", "Русский"),
    ("kk", "Қазақша"),
]

LANGUAGE_COOKIE_NAME = "language"
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Trusted domains
CSRF_TRUSTED_ORIGINS = [
    "https://rr.orleu.edu.kz",
]

# NCANode
NCANODE_URL = os.getenv("NCANODE_URL", "http://localhost:14579/cms/verify")
NCANODE_BASIC_USER = os.getenv("NCANODE_BASIC_USER", "admin")
NCANODE_BASIC_PASS = os.getenv("NCANODE_BASIC_PASS", "admin")

# Deadline
APPLICATION_EDIT_DEADLINE = date(2025, 9, 1)

# Custom error handlers
HANDLER404 = "platformppi.views.handler404"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp-mail.outlook.com"  # или smtp.gmail.com, smtp.mail.ru и т.д.
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "ppi@orleu-edu.kz"
EMAIL_HOST_PASSWORD = "123987Pp"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Настройки Celery
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # URL брокера сообщений
CELERY_ACCEPT_CONTENT = ['json']  # Формат данных
CELERY_TASK_SERIALIZER = 'json'  # Сериализация задач

CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERYD_TASK_TIME_LIMIT = 300  # секунды

# Настройки периодических задач через Django-Celery-Beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Адрес и порт вашего Redis-сервера
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'platformppi',  # Префикс для ключей в Redis
    }
}

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] {name}:{lineno} — {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "when": "midnight",
            "backupCount": 7,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "errors.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 3,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },

        "apps": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        }

    },
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn="https://ff7c4fd39c864e31c7446533d216a993@o4509389031800832.ingest.de.sentry.io/4509389032783952",
    integrations=[DjangoIntegration(), CeleryIntegration()],

    # Вкл. полные данные пользователя (email, id, ip)
    send_default_pii=True,

    # Производительность — отключена (чтобы не грузить лимит)
    traces_sample_rate=0.0,

    # Только ошибки уровня WARNING и выше
    debug=False,

    # Максимально полезно в проде — не отправлять повторяющиеся ошибки за короткий период
    max_breadcrumbs=50,

    # Не включаем "replay" (если только не нужен)
    # _experiments={"profiles_sample_rate": 0.0},

    # Указать окружение
    environment="production",

    # Можно явно указать релиз (например, git hash)
    release="platformppi@2025.05.26",
)
