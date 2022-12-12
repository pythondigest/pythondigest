"""
Base settings to build other settings files upon.
"""
import logging
import os
import sys
from os import path
from pathlib import Path

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

env = environ.Env()

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="^on^)iv65k_8e!!)q3fttt04#3kcy!joqyjon(ti(ij7wlifee",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG", False)

THUMBNAIL_DEBUG = False
VERSION = (1, 0, 0)

BASE_DOMAIN = env("BASE_DOMAIN", default="pythondigest.ru")

ALLOWED_HOSTS = [
    BASE_DOMAIN,
    f"m.{BASE_DOMAIN}",
    f"www.{BASE_DOMAIN}",
    "188.120.227.123",  # new server
    "92.63.107.227",  # old server
    "127.0.0.1",
    "0.0.0.0",
]
if "pythondigest.ru" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("pythondigest.ru")

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env.bool("USE_DOCKER", default=False):
    import socket

    hostname, __, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "admin_reorder",
    "bootstrapform",
    "sorl.thumbnail",
    "letsencrypt",
    "pytils",
    "ckeditor",
    "taggit",
    "taggit_autosuggest",
    "digest",
    "frontend",
    # 'jobs',
    "advertising",
    # 'landings',
    "account",
    "micawber.contrib.mcdjango",
    "compressor",
    "secretballot",
    "likes",
    "django_remdow",
    "siteblocks",
    # css
    "bootstrap3",
]

CACHALOT_ENABLED = env.bool("CACHALOT_ENABLED", False)
if CACHALOT_ENABLED:
    try:
        import cachalot

        INSTALLED_APPS.append("cachalot")
    except ImportError:
        print("WARNING. You activate Cachalot, but i don't find package")


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]


# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
    # "admin_reorder.middleware.ModelAdminReorder",
    "secretballot.middleware.SecretBallotIpUseragentMiddleware",
    "likes.middleware.SecretBallotUserIpUseragentMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
            ],
            "loaders": (
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ),
        },
    },
]

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

WSGI_APPLICATION = "conf.wsgi.application"

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if env("DATABASE_URL", default=None):
    db_settings = env.db("DATABASE_URL")
elif env("POSTGRES_DB", default=None):
    db_settings = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env.int("POSTGRES_PORT"),
    }
else:
    db_settings = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path.join(BASE_DIR, "db.sqlite"),
    }

if "test" in sys.argv:
    db_settings = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_CHARSET": "UTF8",
        "TEST_NAME": ":memory:",
    }

DATABASES = {"default": db_settings}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Aleksandr Sapronov""", "a@sapronov.me")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = "ru-ru"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]
USE_I18N = True
USE_L10N = True
USE_TZ = False
SITE_ID = 1
LOCALE_PATHS = (path.join(BASE_DIR, "locale"),)

# STATIC
# ------------------------
STATIC_URL = "/static/"
STATIC_ROOT = path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = path.join(BASE_DIR, "media")

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
if env("REDIS_URL", default=None):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # Mimicing memcache behavior.
                # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
                "IGNORE_EXCEPTIONS": True,
            },
        },
    }
elif env("MEMCACHED_URL", default=None):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": env("MEMCACHED_URL"),
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

CACHES["site"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "unique-snowflake",
}

CACHE_PAGE_ENABLED = env("CACHE_PAGE_ENABLED", default=True)
CACHE_MIDDLEWARE_ALIAS = "site"  # The cache alias to use for storage and 'default' is **local-memory cache**.
CACHE_MIDDLEWARE_SECONDS = 600  # number of seconds before each page is cached
CACHE_MIDDLEWARE_KEY_PREFIX = ""

if not CACHE_PAGE_ENABLED:
    MIDDLEWARE.remove("django.middleware.cache.FetchFromCacheMiddleware")

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        # display sql requests
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "sendgrid_username"
EMAIL_HOST_PASSWORD = "sendgrid_password"

# ID пользователя от имени когорого будут импортироваться данные
BOT_USER_ID = 11

PROXIES_FOR_GOOGLING = {}
TOR_CONTROLLER_PWD = ""

MICAWBER_PROVIDERS = "micawber.contrib.mcdjango.providers.bootstrap_basic"
# MICAWBER_PROVIDERS = 'micawber.contrib.mcdjango.providers.bootstrap_embedly'
MICAWBER_TEMPLATE_EXTENSIONS = [
    ("oembed_no_urlize", {"urlize_all": False}),
]

# django-browser-reload
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_browser_reload"]
MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            [
                "Undo",
                "Redo",
                "-",
                "Link",
                "Unlink",
                "HorizontalRule",
                "-",
                "BulletedList",
                "NumberedList",
                "PasteText",
                "-",
                "Source",  # 'glvrdPlugin',
            ]
        ],
        # 'extraPlugins': 'glvrdPlugin'
    },
}


DATASET_ROOT = path.join(BASE_DIR, "dataset")
DATASET_FOLDER = ""
DATASET_POSITIVE_KEYWORDS = [
    "blog",
    "article",
    "news-item",
    "section",
    "content",
    "body-content",
    "hentry",
    "entry-content",
    "page-content",
    "readme",
    "markdown-body entry-content",
    "maia-col-6",
    "maia-col-10",
    "col-md-9",
    "col-md-12",
    "maia-article",
    "col-md-6",
    "post_show",
    "content html_format",
    "watch-description-content",
    "watch-description",
    "watch-description-text",
    "article-content",
    "post",
    "container",
    "summary",
    "articleBody",
    "article hentry",
    "article-content",
    "entry-content",
    "viewitem-content",
    "main",
    "post",
    "post-content",
    "section-content",
    "articleBody",
    "section",
    "document",
    "rst-content",
    "markdown-content",
    "wy-nav-content",
    "toc",
    "book",
    "col-md-12",
]

DATASET_NEGATIVE_KEYWORDS = [
    "mysidebar",
    "related",
    "ads",
    "footer",
    "menu",
    "navigation",
    "navbar",
    "404",
    "error 404",
    "error: 404",
    "page not found",
    "file-wrap",
    "navbar",
]

CLS_URL_BASE = ""
CLS_ENABLED = env.bool("CLS_ENABLED", False)

GITTER_TOKEN = env.str("GITTER_TOKEN", default=None)
TWITTER_CONSUMER_KEY = env.str("TWITTER_CONSUMER_KEY", default=None)
TWITTER_CONSUMER_SECRET = env.str("TWITTER_CONSUMER_SECRET", default=None)
TWITTER_TOKEN = env.str("TWITTER_TOKEN", default=None)
TWITTER_TOKEN_SECRET = env.str("TWITTER_TOKEN_SECRET", default=None)
TGM_BOT_ACCESS_TOKEN = env.str("TGM_BOT_ACCESS_TOKEN", default=None)
TGM_CHANNEL = env.str("TGM_CHANNEL", default=None)
IFTTT_MAKER_KEY = env.str("IFTTT_MAKER_KEY", default=None)
# TODO: configure by oauth for pub digest
VK_APP_ID = env.int("VK_APP_ID", default=0)
VK_LOGIN = env.str("VK_LOGIN", default=None)
VK_PASSWORD = env.str("VK_PASSWORD", default=None)

YANDEX_METRIKA_ID = "36284495"

ADMIN_REORDER = (
    "digest",
    "advertising",
    "siteblocks",
    "landings",
    # 'taggit',
    # 'jobs',
    "frontend",
    # 'sites',
    "auth",
    "account",
    "default",
)

HTML_MINIFY = True

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL
LIBSASS_OUTPUT_STYLE = "compressed"
# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}

MAILHANDLER_RU_KEY = ""
MAILHANDLER_RU_USER_LIST_ID = 413

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

CSRF_TRUSTED_ORIGINS = [
    f"https://{BASE_DOMAIN}",
    f"https://m.{BASE_DOMAIN}",
    f"https://www.{BASE_DOMAIN}",
    "https://dev.pythondigest.ru",
]
if "https://pythondigest.ru" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("https://pythondigest.ru")

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN", default=None)
if SENTRY_DSN:
    SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    integrations = [
        sentry_logging,
        DjangoIntegration(),
        RedisIntegration(),
    ]
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        environment=env("SENTRY_ENVIRONMENT", default="default"),
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
    )

if not os.path.isdir(DATASET_ROOT):
    os.makedirs(DATASET_ROOT)

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # 'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

    if "cachalot" in INSTALLED_APPS:
        DEBUG_TOOLBAR_PANELS.append("cachalot.panels.CachalotPanel")
