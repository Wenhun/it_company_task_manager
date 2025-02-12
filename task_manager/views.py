from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from task_manager.models import Task


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    tasks = Task.objects.filter(assignees=request.user.id).order_by("deadline", "priority")
    project = get_user_model().objects.get(pk=request.user.id).team.project.project_name

    context = {
        "tasks": tasks,
        "project": project,
    }

    return render(request, "task_manager/index.html", context=context)
