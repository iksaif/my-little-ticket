# Local settings.
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STORAGE_DIR = os.path.join(ROOT_DIR, 'storage')

SECRET_KEY = 'changeme'
DEBUG = True

ALLOWED_HOSTS = ['*']

JIRA_URL = 'https://jira.com/'
JIRA_USERNAME = os.environ.get('JIRA_USERNAME')
JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')

STATIC_ROOT = os.path.join(os.path.dirname(ROOT_DIR), 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(STORAGE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(STORAGE_DIR, 'cache'),
    }
}
