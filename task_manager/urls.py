from django.urls import path

from task_manager.views import index

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
]