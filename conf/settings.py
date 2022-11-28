# -*- coding: utf-8 -*-
import os
from os import path

BASE_DIR = path.abspath(path.join(path.dirname(__file__), '..'))

SECRET_KEY = 'TBD IN LOCAL SETTINGS'

DEBUG = True

THUMBNAIL_DEBUG = False
VERSION = (1, 0, 0)
ALLOWED_HOSTS = ['pythondigest.ru']

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
    'rosetta',
    'social.apps.django_app.default',
    'micawber.contrib.mcdjango',

    'compressor',

    # TODO - разобраться в зависимостях
    'secretballot',
    'likes',

    'django_remdow',

    'siteblocks',

    'cachalot',

)

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

if DEBUG:
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',)
else:
    MIDDLEWARE_CLASSES = ()

MIDDLEWARE_CLASSES += (
    'django.middleware.cache.UpdateCacheMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'concurrency.middleware.ConcurrencyMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
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
            'django.core.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'account.context_processors.account',
            'social.apps.django_app.context_processors.backends',
            'social.apps.django_app.context_processors.login_redirect',
        ],
        'loaders': (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    },
}, ]

AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',  # ok
    'social.backends.vk.VKOAuth2',  # ok
    'social.backends.twitter.TwitterOAuth',  # ok
    'social.backends.facebook.FacebookOAuth2',  # ok
    # 'social.backends.bitbucket.BitbucketOAuth',
    # 'social.backends.google.GoogleOAuth2',
    # 'social.backends.linkedin.LinkedinOAuth2',
    # 'social.backends.open_id.OpenIdAuth',
    'social.backends.email.EmailAuth', 'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',)

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
LOCALE_PATHS = (path.join(BASE_DIR, 'locale'),)

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
    'social.pipeline.mail.mail_validation', 'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    # 'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',  # 'social.pipeline.debug.debug'
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'

SOCIAL_AUTH_VK_OAUTH2_KEY = ''
SOCIAL_AUTH_VK_OAUTH2_SECRET = ''

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_GOOGLE_OAUTH_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ''

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

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 2,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 10,
    'bulk': 5,
    'orm': 'default'
}

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
        'cachalot.panels.CachalotPanel',
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
