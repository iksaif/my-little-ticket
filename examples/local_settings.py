# Local settings.
import os
import random
import hashlib

SECRET_KEY = hashlib.sha1(str(random.random()).encode())
DEBUG = True

JIRA_URL = 'https://jira.com/'
JIRA_USERNAME = os.environ.get('JIRA_USERNAME')
JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}
