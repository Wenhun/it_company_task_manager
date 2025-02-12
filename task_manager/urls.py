from django.urls import path

from task_manager.views import index, TaskDetailView

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
