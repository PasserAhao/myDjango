try:
    from config.default import *
    from config.celery.config import *
except ImportError:
    pass

MY_APPS += [

]
INSTALLED_APPS += MY_APPS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "kac_saas",
        "USER": "root",
        "PASSWORD": "admin123",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
}
