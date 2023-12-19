from django.urls import path
from .view import tasks

urlpatterns = [
    path('test/', tasks.test),
]
