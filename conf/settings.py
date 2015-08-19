# -*- coding: utf-8 -*-
from os import path

BASE_DIR = path.abspath(path.join(path.dirname(__file__), '..'))

SECRET_KEY = 'TBD IN LOCAL SETTINGS'

DEBUG = False

TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = False

ALLOWED_HOSTS = ['pythondigest.ru']



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap_admin',
    'django.contrib.admin',

    'bootstrapform',
    'sorl.thumbnail',
    'pytils',
    'concurrency',

    'digest',
    'frontend',


    'account',
    'rosetta',
    'social.apps.django_app.default',

)

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'
SOCIAL_AUTH_URL_NAMESPACE = 'social'


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'concurrency.middleware.ConcurrencyMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
)


ROOT_URLCONF = 'conf.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (

    'social.backends.github.GithubOAuth2',  # ok
    'social.backends.vk.VKOAuth2',  # ok
    'social.backends.twitter.TwitterOAuth',  #

    'social.backends.facebook.FacebookOAuth2',

    'social.backends.bitbucket.BitbucketOAuth',


    'social.backends.google.GoogleOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GooglePlusAuth',
    'social.backends.google.GoogleOpenIdConnect',
    'social.backends.instagram.InstagramOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.livejournal.LiveJournalOpenId',
    'social.backends.mailru.MailruOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.open_id.OpenIdAuth',


    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
)


WSGI_APPLICATION = 'conf.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(BASE_DIR, 'db.sqlite'),
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile'
]


TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = True
USE_TZ = False
SITE_ID = 1
LOCALE_PATHS = (
    path.join(BASE_DIR, 'locale'),
)

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)



CONCURRENCY_HANDLER409 = 'digest.views.conflict'
CONCURRENCY_POLICY = 2  # CONCURRENCY_LIST_EDITABLE_POLICY_ABORT_ALL


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sendgrid_username'
EMAIL_HOST_PASSWORD = 'sendgrid_password'

# ID пользователя от имени когорого будут импортироваться данные
BOT_USER_ID = 11

PROXIES_FOR_GOOGLING = {}
TOR_CONTROLLER_PWD = ''

BASE_DOMAIN = 'pythondigest.ru'


# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'conf.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'conf.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug'
)


SOCIAL_AUTH_VK_OAUTH2_KEY = ''
SOCIAL_AUTH_VK_OAUTH2_SECRET = ''

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

try:
    from .local_settings import *
except ImportError:
    pass
