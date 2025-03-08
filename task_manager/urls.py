from django.urls import path

from task_manager.views import (
    IndexView,
    TaskDetailView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    CategoriesView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    SetTaskAsCompletedView,
)

app_name = "task_manager"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"),
    path(
        "projects/",
        ProjectListView.as_view(),
        name="project-list"),
    path(
        "projects/create",
        ProjectCreateView.as_view(),
        name="project-create"),
    path(

        "projects/<int:pk>/update",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "projects/<int:pk>/delete",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"),
    path(
        "workers/creation/",
        WorkerCreateView.as_view(),
        name="worker-create"),
    path(
        "workers/<int:pk>/update",
        WorkerUpdateView.as_view(),
        name="worker-update"),
    path(
        "workers/<int:pk>/delete",
        WorkerDeleteView.as_view(),
        name="worker-delete"),
    path(
        "teams/",
        TeamListView.as_view(),
        name="team-list"),
    path(
        "teams/<int:pk>/",
        TeamDetailView.as_view(),
        name="team-detail"),
    path(
        "teams/create/",
        TeamCreateView.as_view(),
        name="team-create"),
    path(
        "teams/<int:pk>/update",
        TeamUpdateView.as_view(),
        name="team-update"),
    path(
        "teams/<int:pk>/delete",
        TeamDeleteView.as_view(),
        name="team-delete"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path(
        "categories/task_type/create",
        TaskTypeCreateView.as_view(),
        name="categories-task-type-create",
    ),
    path(
        "categories/task_type/<int:pk>/update",
        TaskTypeUpdateView.as_view(),
        name="categories-task-type-update",
    ),
    path(
        "categories/task_type/<int:pk>/delete",
        TaskTypeDeleteView.as_view(),
        name="categories-task-type-delete",
    ),
    path(
        "categories/position/create",
        PositionCreateView.as_view(),
        name="categories-position-create",
    ),
    path(
        "categories/position/<int:pk>/update",
        PositionUpdateView.as_view(),
        name="categories-position-update",
    ),
    path(
        "categories/position/<int:pk>/delete",
        PositionDeleteView.as_view(),
        name="categories-position-delete",
    ),
    path(
        "categories/tasks/<int:pk>/set_task_as_completed",
        SetTaskAsCompletedView.as_view(),
        name="set-task-as-completed",
    ),
]
