from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Project, TaskType, Position, Team


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "assignees",
            "task_type",
            "project",
        ]
        widgets = {
            "name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "description":
                forms.Textarea(attrs={"class": "w3-input w3-border"}),
            "deadline":
                forms.DateInput(attrs={"class": "w3-input w3-border"}),
            "priority":
                forms.Select(attrs={"class": "w3-select w3-border"}),
            "assignees":
                forms.Select(attrs={"class": "w3-select w3-border"}),
            "task_type":
                forms.Select(attrs={"class": "w3-select w3-border"}),
            "project":
                forms.Select(attrs={"class": "w3-select w3-border"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "project_name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "description":
                forms.Textarea(attrs={"class": "w3-input w3-border"}),
            "budget":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "deadline":
                forms.DateInput(attrs={"class": "w3-input w3-border"}),
            "status":
                forms.Select(attrs={"class": "w3-select w3-border"}),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"
        widgets = {
            "name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
        widgets = {
            "name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
        }


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "team",
            "is_team_lead",
        )

        widgets = {
            "username":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "password":
                forms.PasswordInput(attrs={"class": "w3-password w3-border"}),
            "first_name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "last_name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "position":
                forms.Select(attrs={"class": "w3-select w3-border"}),
            "team":
                forms.Select(attrs={"class": "w3-select w3-border"}),
            "is_team_lead":
                forms.CheckboxInput(attrs={"class": "w3-check w3-border"}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
        widgets = {
            "name":
                forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "project":
                forms.Select(attrs={"class": "w3-select w3-border"}),
            "description":
                forms.Textarea(attrs={"class": "w3-input w3-border"}),
        }


class SearchForm(forms.Form):
    def __init__(self, field_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["search_field"].widget.attrs[
            "placeholder"
        ] = f"Search by {field_name}"

    search_field = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"class": "w3-input w3-border"}),
    )
