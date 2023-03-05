import os
import pytest
import django
from django.conf import settings
from django.test import Client


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    settings.DEBUG = False
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    settings.MEDIA_ROOT = '/tmp/app/media/'
    settings.MEDIA_URL = '/media/'


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    django.setup()


@pytest.fixture(scope='function')
def client():
    return Client()