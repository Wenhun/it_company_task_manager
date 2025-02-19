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
    class PriorityChoices(models.IntegerChoices):
        HIGH = 1, "High"
        MEDIUM = 2, "Medium"
        LOW = 3, "Low"

    class Meta:
        ordering = ["deadline", "priority"]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM
    )
    task_type = models.ForeignKey(TaskType,
                                  on_delete=models.CASCADE,
                                  related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="tasks")
    project = models.ForeignKey("Project",
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name="tasks")

    def __str__(self):
        workers = ", ".join([str(worker) for worker in self.assignees.all()])

        if self.is_completed:
            return f"{self.name}: Completed! Workers: {workers}"
        else:
            return (f"{self.name}: Not Completed! "
                    f"Priority: {self.priority}, "
                    f"Deadline={self.deadline}, "
                    f"Workers: {workers}")


class Project(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "Active", "Active"
        COMPLETED = "Completed", "Completed"
        CANCELED = "Canceled", "Canceled"
        ON_HOLD = "On Hold", "On Hold"

    project_name = models.CharField(max_length=255)
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
    is_team_lead = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

    def __str__(self) -> str:
        return (f"{self.username}: "
                f"({self.first_name} {self.last_name})"
                f"Position: {self.position.name}")
