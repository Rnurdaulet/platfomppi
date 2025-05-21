import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-3jp6k1kvrw+r!c18kjj17=f8d#)+o+=5o!=25=*_az9$s_dlgt'

from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv("DEBUG", "0") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'whitenoise',

    'apps.accounts',
    'apps.lookups',
    'apps.contest',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = "accounts.User"

ROOT_URLCONF = 'platfomppi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'platfomppi.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv("POSTGRES_DB"),
#         'USER': os.getenv("POSTGRES_USER"),
#         'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Aqtobe'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("ru", "Русский"),
    ("kk", "Қазақша"),
]
LANGUAGE_COOKIE_NAME = 'language'

LOCALE_PATHS = [BASE_DIR / "locale"]



LOGIN_URL = "/login/ecp/"          # или /login/, если у тебя есть логин по паролю
LOGIN_REDIRECT_URL = "/"           # куда редирект после успешного входа
LOGOUT_REDIRECT_URL = "/"          # после logout()


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # откуда collectstatic будет брать файлы
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    "https://rr.orleu.edu.kz",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

NCANODE_URL = os.getenv("NCANODE_URL", "http://localhost:14579/cms/verify")
NCANODE_BASIC_USER = os.getenv("NCANODE_BASIC_USER", "admin")
NCANODE_BASIC_PASS = os.getenv("NCANODE_BASIC_PASS", "admin")


HANDLER404 = "platfomppi.views.handler404"