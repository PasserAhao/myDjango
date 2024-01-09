try:
    from config import *
    from config.default import *
    from config.celery.config import *
except ImportError:
    pass

MY_APPS = [
    'apps.celeryDemo.apps.CeleryTaskDemo',
    'baseserver.apps.BaseServer',
]

INSTALLED_APPS += MY_APPS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mbg",
        "USER": "root",
        "PASSWORD": "admin123",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
}
try:
    from local_settings import *
except ImportError:
    pass
