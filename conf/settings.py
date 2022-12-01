# -*- coding: utf-8 -*-
import os
from os import path

BASE_DIR = path.abspath(path.join(path.dirname(__file__), '..'))

SECRET_KEY = 'TBD IN LOCAL SETTINGS'

DEBUG = True

THUMBNAIL_DEBUG = False
VERSION = (1, 0, 0)
ALLOWED_HOSTS = ['pythondigest.ru', "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'controlcenter',

    'admin_reorder',
    'bootstrapform',
    'sorl.thumbnail',
    'pytils',
    'concurrency',

    'ckeditor',

    'taggit',
    'taggit_autosuggest',

    'digest',
    'frontend',
    'jobs',
    'advertising',
    'landings',

    'account',
    'micawber.contrib.mcdjango',

    'compressor',

    # TODO - разобраться в зависимостях
    'secretballot',
    'likes',

    'django_remdow',

    'siteblocks',

)

try:
    import cachalot
    INSTALLED_APPS += ('cachalot', )
except ImportError:
    pass

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

if DEBUG:
    MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',)
else:
    MIDDLEWARE = ()

MIDDLEWARE += (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'concurrency.middleware.ConcurrencyMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    # 'admin_reorder.middleware.ModelAdminReorder',
    'secretballot.middleware.SecretBallotIpUseragentMiddleware',
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
)

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
    ],
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'account.context_processors.account',
        ],
        'loaders': (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    },
}, ]

AUTHENTICATION_BACKENDS = (
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

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = True
USE_TZ = False
SITE_ID = 1
LOCALE_PATHS = (path.join(BASE_DIR, 'locale'),)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')

DATASET_ROOT = path.join(BASE_DIR, 'dataset')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',

)

CONCURRENCY_HANDLER409 = 'digest.views.conflict'
CONCURRENCY_POLICY = 2  # CONCURRENCY_LIST_EDITABLE_POLICY_ABORT_ALL

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':
            {'handlers': ['mail_admins'],
             'level': 'ERROR',
             'propagate': True, },
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

MICAWBER_PROVIDERS = 'micawber.contrib.mcdjango.providers.bootstrap_basic'
# MICAWBER_PROVIDERS = 'micawber.contrib.mcdjango.providers.bootstrap_embedly'
MICAWBER_TEMPLATE_EXTENSIONS = [
    ('oembed_no_urlize', {'urlize_all': False}),
]

CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Link', 'Unlink', 'HorizontalRule',
             '-', 'BulletedList', 'NumberedList', 'PasteText',
             '-', 'Source',  # 'glvrdPlugin',
             ]
        ],
        # 'extraPlugins': 'glvrdPlugin'

    },

}

DATASET_FOLDER = ''
DATASET_POSITIVE_KEYWORDS = list({
    'blog',
    'article',
    'news-item',
    'section',
    'content',
    'body-content',
    'hentry',
    'entry-content',
    'page-content',
    'readme',
    'markdown-body entry-content',
    'maia-col-6',
    'maia-col-10',
    'col-md-9',
    'col-md-12',
    'maia-article',
    'col-md-6',
    'post_show',
    'content html_format',
    'watch-description-content',
    'watch-description',
    'watch-description-text',
    'article-content',
    'post',
    'container',
    'summary',
    'articleBody',
    'article hentry',
    'article-content',
    'entry-content',
    'viewitem-content',
    'main',
    'post',
    'post-content',
    'section-content',
    'articleBody',
    'section',
    'document',
    'rst-content',
    'markdown-content',
    'wy-nav-content',
    'toc',
    'book',
    'col-md-12',

})

DATASET_NEGATIVE_KEYWORDS = list({
    "mysidebar",
    "related",
    "ads",
    'footer',
    'menu',
    'navigation',
    'navbar',
    '404',
    'error 404',
    'error: 404',
    'page not found',
    'file-wrap',
    'navbar',
})

CLS_URL_BASE = ''

GITTER_TOKEN = ''
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_TOKEN = ''
TWITTER_TOKEN_SECRET = ''
TGM_BOT_ACCESS_TOKEN = ''
TGM_CHANNEL = ''
IFTTT_MAKER_KEY = ''
VK_APP_ID = 0
VK_LOGIN = ''
VK_PASSWORD = ''

ADMIN_REORDER = (
    'digest',
    'advertising',
    # 'controlcenter',
    'siteblocks',
    'landings',
    # 'taggit',
    # 'jobs',

    'frontend',

    # 'sites',
    'auth',
    # 'account',
    'default',

)

CONTROLCENTER_DASHBOARDS = (
    'digest.dashboards.MyDashboard',
)

ALCHEMY_KEY = ''
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
)

MAILHANDLER_RU_KEY = ''
MAILHANDLER_RU_USER_LIST_ID = 413

HTML_MINIFY = True
try:
    from .local_settings import *
except ImportError as e:
    print("Warning. Not found local settings: {}".format(str(e)))

if not os.path.isdir(DATASET_ROOT):
    os.makedirs(DATASET_ROOT)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        # 'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

    if "cachalot" in INSTALLED_APPS:
        DEBUG_TOOLBAR_PANELS.append('cachalot.panels.CachalotPanel')
