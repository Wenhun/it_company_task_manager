from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from task_manager.models import Task, Project, Team


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    current_user_id = request.user.id
    tasks = Task.objects.prefetch_related("assignees").filter(assignees=current_user_id)
    tasks = tasks.order_by("deadline", "priority")
    project = get_user_model().objects.get(pk=current_user_id).team.project
    num_completed_tasks = tasks.filter(is_completed=True).count()
    num_not_completed_tasks = tasks.filter(is_completed=False).count()
    team_workers = (
        get_user_model()
        .objects.filter(team=request.user.team)
        .exclude(id=current_user_id)
    )
    current_date = datetime.now().date()

    context = {
        "tasks": tasks,
        "project": project,
        "num_completed_tasks": num_completed_tasks,
        "num_not_completed_tasks": num_not_completed_tasks,
        "team_workers": team_workers,
        "current_date": current_date,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.now()
        task = context["task"]
        days_difference = (current_date.date() - task.deadline).days
        context["days_difference"] = days_difference
        context["is_overdue"] = days_difference > 0
        return context


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class TasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.now().date()
        return context
