try:
    from config import *
    from config.default import *
    from config.celery.config import *
except ImportError:
    pass

MY_APPS = [
    'apps.celery_task_test.apps.CeleryTaskTest',
    'commands.apps.CommandConfig',
]

INSTALLED_APPS += MY_APPS

try:
    from local_settings import *
except ImportError:
    pass
