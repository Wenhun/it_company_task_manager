from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from task_manager.models import Task, Project


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    current_user_id = request.user.id
    tasks = Task.objects.prefetch_related("assignees").filter(
        assignees=current_user_id)
    tasks = tasks.order_by("deadline", "priority")
    project = get_user_model().objects.get(
        pk=current_user_id).team.project.project_name
    num_completed_tasks = tasks.filter(is_completed=True).count()
    num_not_completed_tasks = tasks.filter(is_completed=False).count()

    context = {
        "tasks": tasks,
        "project": project,
        "num_completed_tasks": num_completed_tasks,
        "num_not_completed_tasks": num_not_completed_tasks,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
