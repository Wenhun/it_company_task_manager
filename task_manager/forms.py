from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Task


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "assignees", "task_type", "project"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "description": forms.Textarea(attrs={"class": "w3-input w3-border"}),
            "deadline": forms.DateInput(attrs={"class": "w3-input w3-border"}),
            "priority": forms.Select(attrs={"class": "w3-select w3-border"}),
            "assignees": forms.Select(attrs={"class": "w3-select w3-border"}),
            "task_type": forms.Select(attrs={"class": "w3-select w3-border"}),
            "project": forms.Select(attrs={"class": "w3-select w3-border"}),
        }
