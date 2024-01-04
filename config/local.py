from config.default import *

try:
    from config.celery.config import *
except ImportError:
    pass

MY_APPS += [
    'health_check',  # required
    'health_check.db',  # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.celery',  # requires celery
    'health_check.contrib.celery_ping',  # requires celery
    'health_check.contrib.psutil',  # disk and memory utilization; requires psutil
    'health_check.contrib.s3boto3_storage',  # requires boto3 and S3BotoStorage backend
    'health_check.contrib.rabbitmq',  # requires RabbitMQ broker
    'health_check.contrib.redis',  # requires Redis broker
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

HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # percent
    'MEMORY_MIN': 100,  # in MB
}

HEALTH_CHECK = {
    # .....
    "SUBSETS": {
        "startup-probe": ["MigrationsHealthCheck", "DatabaseBackend"],
        "liveness-probe": ["DatabaseBackend"],
        "<SUBSET_NAME>": ["<Health_Check_Service_Name"]
    },
    # .....
}

try:
    from local_settings import *
except ImportError:
    pass
