import pytest
from django.test import Client
from apps.celery_task_test.celery_task import print_num


@pytest.mark.test
def test_print_num_view():
    client = Client()
    res = client.get("/celery/test/")
    assert res.status_code == 200


@pytest.mark.local
def test_print_num():
    assert print_num.delay("test")
