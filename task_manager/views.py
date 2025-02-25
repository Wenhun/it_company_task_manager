from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import TaskForm, ProjectForm, TaskTypeForm, PositionForm, WorkerCreationForm, TeamForm, SearchForm
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
        name = self.request.GET.get("search_field", "")
        context["current_date"] = datetime.now().date()
        context["search_form"] = SearchForm(
            initial={"search_field": name}, field_name="name"
        )
        return context


    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all()
        form = SearchForm(data=self.request.GET, field_name="name")
        if form.is_valid():
            if self.request.GET.get("overdue") == "true":
                queryset = queryset.filter(deadline__lt=datetime.now().date())

            return queryset.filter(
                name__icontains=form.cleaned_data["search_field"])

        return queryset


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "project_list"
    template_name = "task_manager/project_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.now().date()
        project_name = self.request.GET.get("search_field", "")
        context["search_form"] = SearchForm(
            initial={"search_field": project_name}, field_name="project_name"
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Project.objects.all()
        form = SearchForm(data=self.request.GET, field_name="project_name")
        if form.is_valid():
            return queryset.filter(
                project_name__icontains=form.cleaned_data["search_field"])

        return queryset


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("search_field", "")
        context["search_form"] = SearchForm(
            initial={"search_field": username}, field_name="username"
        )
        return context


    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.all()
        form = SearchForm(data=self.request.GET, field_name="username")
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["search_field"])

        return queryset


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


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task_manager:categories")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task_manager:categories")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:categories")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:categories")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:categories")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:categories")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        worker = form.instance
        self.success_url = reverse("task_manager:worker-detail", kwargs={'pk': worker.pk})
        return response


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerCreationForm

    def get_success_url(self):
        return self.request.POST.get("next", "/")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:worker-list")


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task_manager:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task_manager:team-list")


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")
