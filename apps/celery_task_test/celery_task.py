from celery import shared_task


@shared_task
def print_num(data=None):
    if not data:
        data = "没有传入参数哦"
    print(data)
