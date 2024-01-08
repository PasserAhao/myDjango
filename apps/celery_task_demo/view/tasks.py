import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from apps.celery_task_test.celery_task import print_num


def test(request):
    print(request.GET)
    print_num.delay("这个是普通任务")
    print_num.apply_async(args=("这个是延迟任务",), eta=(datetime.now() + timedelta(seconds=10)))
    return HttpResponse(json.dumps({
        "code": 0,
        "msg": "OK",
    }))
