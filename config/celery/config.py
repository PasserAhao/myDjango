from kombu import Queue, Exchange
from celery.schedules import crontab

CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
CELERY_BEAT_SCHEDULE = {
    'task1': {
        'task': 'apps.celeryDemo.celery_task.print_num',
        'schedule': 10,  # 每隔 10 秒执行一次
        'args': {"十秒执行一次", },
        'options': {
            'queue': 'task1'
        }
    },
    'task2': {
        'task': 'apps.celeryDemo.celery_task.print_num',
        'schedule': crontab(hour=10, minute=17),
        'args': {"这个是定时任务", },
        'options': {
            'queue': 'task2'
        }
    },
}

CELERY_IMPORTS = (
    "apps.celeryDemo.celery_task",
)

DEFAULT_EXCHANGE = Exchange("default_exchange", type="direct")

CELERY_TASK_DEFAULT_QUEUE = 'task1'
CELERY_TASK_QUEUES = (
    Queue("task1", DEFAULT_EXCHANGE, routing_key="task1"),
    Queue("task2", DEFAULT_EXCHANGE, routing_key="task2"),
)

CELERY_TASK_ROUTES = {
    "apps.celeryDemo.celery_task.*": {
        "queue": "task1",
        "routing_key": "task1"
    },
}
# Celery作为第三方模块集成到项目中，在全局配置中添加
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Redis Key添加前缀，便于管理
CELERY_BROKER_TRANSPORT_OPTIONS = {'global_keyprefix': 'celery:'}

# 避免死锁
CELERYD_FORCE_EXECV = True

# 设置失败允许重试（这个慎用，如果失败任务无法再次执行成功，会产生指数级别的失败记录。即，任务失败会再回滚任务到队列中，造成队列中同一任务指数性增加）
# 如果设置了True，必须在异步任务中指定失败重试的次数
CELERY_ACKS_LATE = False

# 单个任务的最大运行时间，超时会被杀死（慎用，有大文件操作、长时间上传、下载任务时，需要关闭这个选项，或者设置更长时间）
CELERYD_TIME_LIMIT = 10 * 60

# 每个worker工作进程最多执行500个任务被销毁，可以防止内存泄漏，500是举例，根据自己的服务器的性能可以调整数值
CELERYD_MAX_TASKS_PER_CHILD = 500

# 设置并发worker数量
CELERYD_WORKER_CONCURRENCY = 2

# celery 任务结果内容格式
CELERYD_ACCEPT_CONTENT = ['json']

# 任务发出后，经过一段时间还未收到acknowledge ，就将任务重新交给其他worker执行
CELERYD_WORKER_DISABLE_RATE_LIMITS: True

# 时区设置（注意这里可能会导致定时任务不在规定时间执行）
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
