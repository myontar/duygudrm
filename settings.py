# Django settings for testproj2 project.
# -*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'ddgo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        #'SUPPORTS_TRANSACTIONS': False,
    },
}
CACHE_BACKEND = 'memcached://128.0.0.1:11211/'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'tr-tr'

ugettext = lambda s: s

LANGUAGES = (
    ('de', 'German'),
    ('tr', 'Turkish'),
    ('en', 'English'),
)
LOCALE_PATHS ="locale/"
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ju^y4b6j4w%)346pf8oxbw=po8)-)hd3ugq=jjw4x38ugf#_0c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n'

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
        'django.contrib.auth.backends.ModelBackend',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
   'django.middleware.locale.LocaleMiddleware'
   )

ROOT_URLCONF = 'duygudrm.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
<<<<<<< HEAD
    "/var/ftp/virtual_users/framemind/http/duygudrm/layouts/"
=======
    "/home/django/duygudrm/layouts/"
>>>>>>> 243e70bd7b01e3cc9c701cb812b05c4ef8954599
)

INSTALLED_APPS = (
#    'django_mongodb_engine',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'duygudrm.ddapp',
    'duygudrm.wrap',
    'django.contrib.admin',
    'djangotoolbox'
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'duygudrm.ddapp.models.MyLoginBackend', # if they fail the normal test
 )

WRAP_URLS = {
             'consent': 'https://consent.live.com/Connect.aspx',
             'access':'https://consent.live.com/AccessToken.aspx',
             'refresh': 'https://consent.live.com/RefreshToken.aspx'
}
# Default scope for the applicaiton
LIVE_DEFAULT_SCOPE = 'WL_Profiles.View,WL_Contacts.View'

# Application Specific Globals that identify your applicaiton
<<<<<<< HEAD
LIVE_APP_ID = '000000004C03A91E'
LIVE_APP_SECRET = 'dkiGnkkZSFmCA7Itk6vKJLi1bw3qygC6'
LIVE_DEFAULT_CALLBACK = 'http://framemind.com/messenger/OAuthResponseHandler'
=======
LIVE_APP_ID = '000000004404100D'
LIVE_APP_SECRET = 'n5dCsni5eDOHF4QTYzhYhbhAONbvYerB'
LIVE_DEFAULT_CALLBACK = 'http://mstfyntr.com:88/messenger/OAuthResponseHandler'
>>>>>>> 243e70bd7b01e3cc9c701cb812b05c4ef8954599
