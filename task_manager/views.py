from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm, ProjectForm
from task_manager.models import Task, Project, Team, TaskType, Position


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    current_user_id = request.user.id
    tasks = Task.objects.prefetch_related("assignees").filter(assignees=current_user_id)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.now()
        task = context["project"]
        days_difference = (current_date.date() - task.deadline).days
        context["days_difference"] = days_difference
        context["is_overdue"] = days_difference > 0
        context["current_date"] = current_date.date()
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.now().date()
        return context


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "project_list"
    template_name = "task_manager/project_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.now().date()
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return self.request.POST.get("next", "/")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:project-list")



class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    context_object_name = "worker_list"
    template_name = "task_manager/worker_list.html"
    paginate_by = 20


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.all().prefetch_related("tasks__task_type")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.now().date()
        context["tasks"] = Task.objects.prefetch_related("assignees").filter(
            assignees=context["worker"].id
        )
        return context


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"
    template_name = "task_manager/team_list.html"
    paginate_by = 20


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


@login_required
def categories(request: HttpRequest) -> HttpResponse:
    task_types = TaskType.objects.all()
    positions = Position.objects.all()

    context = {
        "task_types": task_types,
        "positions": positions,
    }

    return render(request, "task_manager/category.html", context=context)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_initial(self):
        initial = super().get_initial()
        worker_id = self.request.GET.get("worker_id")
        project_id = self.request.GET.get("project_id")
        if worker_id:
            worker = get_object_or_404(get_user_model(), id=worker_id)
            initial["assignees"] = [worker]

        if project_id:
            project = get_object_or_404(Project, id=project_id)
            initial["project"] = project

        return initial

    def get_success_url(self):
        return self.request.POST.get("next", "/")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return self.request.POST.get("next", "/")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
