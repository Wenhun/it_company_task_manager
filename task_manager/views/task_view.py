from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm, SearchForm
from task_manager.models import Task, Project


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
                queryset = queryset.filter(deadline__lt=datetime.now().date(),
                                           is_completed=False)

            if self.request.GET.get("hide_completed") == "true":
                queryset = queryset.filter(is_completed=False)

            return queryset.filter(
                name__icontains=form.cleaned_data["search_field"])

        return queryset


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


@login_required
def set_task_as_completed(request, pk):
    task = Task.objects.get(pk=pk)
    task.is_completed = True
    task.save()
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail",
                                             args=[pk]))
