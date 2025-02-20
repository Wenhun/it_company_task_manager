from django.urls import path

from task_manager.views import (index,
                                TaskDetailView,
                                TasksListView,
                                ProjectDetailView,
                                ProjectListView,
                                WorkerListView,
                                WorkerDetailView,
                                TeamListView)

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/", TasksListView.as_view(), name="task-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("teams/", TeamListView.as_view(), name="team-list"),
]
