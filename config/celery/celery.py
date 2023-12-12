import os
from celery import Celery, platforms
from django.conf import settings

# 启动命令
# celery -A config.celery  worker -l info
# celery -A config.celery  beat -l info

platforms.C_FORCE_ROOT = True
# 告诉celery, django的配置路径在哪里, 方便celery读取配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered my app configs.
app.autodiscover_tasks(lambda: settings.MY_APPS)
