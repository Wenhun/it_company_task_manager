from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import SearchForm, WorkerCreationForm
from task_manager.models import Task


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.all().prefetch_related(
        "tasks__task_type")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.now().date()
        tasks = Task.objects.prefetch_related("assignees").filter(
            assignees=context["worker"].id
        )
        context["num_all_tasks"] = tasks.count()
        not_completed_tasks = tasks.filter(is_completed=False)
        context["not_completed_tasks"] = not_completed_tasks
        context["num_not_completed_tasks"] = not_completed_tasks.count()
        completed_tasks = tasks.filter(is_completed=True)
        context["completed_tasks"] = completed_tasks
        context["num_completed_tasks"] = completed_tasks.count()
        return context


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


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        worker = form.instance
        self.success_url = reverse("task_manager:worker-detail",
                                   kwargs={'pk': worker.pk})
        return response


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerCreationForm

    def get_success_url(self):
        return self.request.POST.get("next", "/")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:worker-list")
