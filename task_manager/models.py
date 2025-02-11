from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM
    )
    task_type = models.ForeignKey(TaskType,
                                  on_delete=models.CASCADE,
                                  related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="tasks")

    def __str__(self):
        return f"{self.name}: priority: {self.priority}"


class Project(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "Active", "Active"
        COMPLETED = "Completed", "Completed"
        CANCELED = "Canceled", "Canceled"
        ON_HOLD = "On Hold", "On Hold"

    project_name = models.CharField(max_length=255)
    tasks = models.ManyToManyField(Task, related_name="projects")
    deadline = models.DateField()
    budget = models.DecimalField(max_digits=12,
                                 decimal_places=2,
                                 null=True,
                                 blank=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.project_name}, status: {self.status}"


class Team(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="teams")
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE,
                                 related_name="workers")
    team = models.ForeignKey(Team,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name="workers")
    team_lead = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

    def __str__(self) -> str:
        return (f"{self.username}: "
                f"({self.first_name} {self.last_name})"
                f"Position: {self.position.name}")
