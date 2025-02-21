from django.urls import path

from task_manager.views import (index,
                                TaskDetailView,
                                TaskListView,
                                TaskCreateView,
                                TaskUpdateView,
                                TaskDeleteView,
                                ProjectDetailView,
                                ProjectListView,
                                WorkerListView,
                                WorkerDetailView,
                                TeamListView,
                                TeamDetailView,
                                categories)

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("categories/", categories, name="categories"),
]
