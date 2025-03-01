from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import SearchForm, ProjectForm
from task_manager.models import Project


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