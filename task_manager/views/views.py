from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import (
    TaskTypeForm,
    PositionForm)

from task_manager.models import (
    Task,
    TaskType,
    Position)


CATEGORIES_URL = reverse_lazy("task_manager:categories")


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    current_user_id = request.user.id

    tasks = Task.objects.prefetch_related(
        "assignees").filter(assignees=current_user_id)
    project = get_user_model().objects.get(pk=current_user_id).team.project

    num_completed_tasks = tasks.filter(is_completed=True).count()
    num_not_completed_tasks = tasks.filter(is_completed=False).count()

    team_workers = (
        get_user_model()
        .objects.filter(team=request.user.team)
        .exclude(id=current_user_id)
    )

    project_tasks = Task.objects.filter(project=project)
    percentage_complete_project = round(
        project_tasks.filter(is_completed=True).count()
        / project_tasks.filter(is_completed=False).count() * 100, 2)

    context = {
        "tasks": tasks,
        "project": project,
        "num_completed_tasks": num_completed_tasks,
        "num_not_completed_tasks": num_not_completed_tasks,
        "team_workers": team_workers,
        "current_date": datetime.now().date(),
        "percentage_complete_project": percentage_complete_project
    }

    return render(request, "task_manager/index.html", context=context)


@login_required
def categories(request: HttpRequest) -> HttpResponse:
    """View function for display Position and TaskType models on one page."""
    task_types = TaskType.objects.all()
    positions = Position.objects.all()

    context = {
        "task_types": task_types,
        "positions": positions,
    }

    return render(request,
                  "task_manager/category.html",
                  context=context)


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy()


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = CATEGORIES_URL


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = CATEGORIES_URL


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = CATEGORIES_URL


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = CATEGORIES_URL


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = CATEGORIES_URL
