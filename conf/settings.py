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
    'social.backends.amazon.AmazonOAuth2',
    'social.backends.angel.AngelOAuth2',
    'social.backends.aol.AOLOpenId',
    'social.backends.appsfuel.AppsfuelOAuth2',
    'social.backends.beats.BeatsOAuth2',
    'social.backends.behance.BehanceOAuth2',
    'social.backends.belgiumeid.BelgiumEIDOpenId',
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.box.BoxOAuth2',
    'social.backends.clef.ClefOAuth2',
    'social.backends.coinbase.CoinbaseOAuth2',
    'social.backends.coursera.CourseraOAuth2',
    'social.backends.dailymotion.DailymotionOAuth2',
    'social.backends.disqus.DisqusOAuth2',
    'social.backends.douban.DoubanOAuth2',
    'social.backends.dropbox.DropboxOAuth',
    'social.backends.dropbox.DropboxOAuth2',
    'social.backends.eveonline.EVEOnlineOAuth2',
    'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.fedora.FedoraOpenId',
    'social.backends.fitbit.FitbitOAuth',
    'social.backends.flickr.FlickrOAuth',
    'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GooglePlusAuth',
    'social.backends.google.GoogleOpenIdConnect',
    'social.backends.instagram.InstagramOAuth2',
    'social.backends.jawbone.JawboneOAuth2',
    'social.backends.kakao.KakaoOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.live.LiveOAuth2',
    'social.backends.livejournal.LiveJournalOpenId',
    'social.backends.mailru.MailruOAuth2',
    'social.backends.mendeley.MendeleyOAuth',
    'social.backends.mendeley.MendeleyOAuth2',
    'social.backends.mineid.MineIDOAuth2',
    'social.backends.mixcloud.MixcloudOAuth2',
    'social.backends.nationbuilder.NationBuilderOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'social.backends.persona.PersonaAuth',
    'social.backends.podio.PodioOAuth2',
    'social.backends.rdio.RdioOAuth1',
    'social.backends.rdio.RdioOAuth2',
    'social.backends.readability.ReadabilityOAuth',
    'social.backends.reddit.RedditOAuth2',
    'social.backends.runkeeper.RunKeeperOAuth2',
    'social.backends.skyrock.SkyrockOAuth',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.spotify.SpotifyOAuth2',
    'social.backends.stackoverflow.StackoverflowOAuth2',
    'social.backends.steam.SteamOpenId',
    'social.backends.stocktwits.StocktwitsOAuth2',
    'social.backends.stripe.StripeOAuth2',
    'social.backends.suse.OpenSUSEOpenId',
    'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    'social.backends.trello.TrelloOAuth',
    'social.backends.tripit.TripItOAuth',
    'social.backends.tumblr.TumblrOAuth',
    'social.backends.twilio.TwilioAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.vk.VKOAuth2',
    'social.backends.weibo.WeiboOAuth2',
    'social.backends.wunderlist.WunderlistOAuth2',
    'social.backends.xing.XingOAuth',
    'social.backends.yahoo.YahooOAuth',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.yammer.YammerOAuth2',
    'social.backends.yandex.YandexOAuth2',
    'social.backends.vimeo.VimeoOAuth1',
    'social.backends.lastfm.LastFmAuth',
    'social.backends.moves.MovesOAuth2',
    'social.backends.vend.VendOAuth2',
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

try:
    from .local_settings import *
except ImportError:
    pass
