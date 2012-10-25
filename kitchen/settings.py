"""Django settings for the Kitchen project"""
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Kitchen settings #
REPO_BASE_PATH = os.path.join(BASE_PATH, "dashboard")
REPO = {
    'NAME': "testrepo",
    'URL': "",
    'SYNC_PERIOD': 2,  # minutes
    'KITCHEN_SUBDIR': '',
    'EXCLUDE_ROLE_PREFIX': 'env',
    'DEFAULT_ENV': 'production',
    'DEFAULT_VIRT': 'guest',
}

COLORS = [
    "#FCD975", "#9ACEEB", "/blues5/1", "#97CE8A", "#FFA764", "#FBC6FF"
]

TAG_CLASSES = {
    "WIP": "btn-danger",
    "dummy": "btn-danger",
}

SHOW_VIRT_VIEW = True
SHOW_HOST_NAMES = True

LOG_FILE = '/tmp/kitchen.log'
SYNCDATE_FILE = '/tmp/kitchen-syncdate'
###################

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/null',
    }
}

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(BASE_PATH, 'dashboard', 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'i#5u!2+wpw+4&8tzom)&@-4p(h4jai7#)r5@^i=sl%_-8-2mb*'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'kitchen.urls'

TEMPLATE_DIRS = (
    BASE_PATH + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "kitchen.dashboard",
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
