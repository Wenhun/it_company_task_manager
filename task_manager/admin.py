from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_manager.models import (Worker,
                                 Team,
                                 Position,
                                 TaskType,
                                 Task,
                                 Project)


admin.site.unregister(Group)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",
                                             "team",
                                             "is_team_lead",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",
                                         "team",
                                         "is_team_lead",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "team",
                        "is_team_lead",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",
                    "description",
                    "deadline",
                    "is_completed",
                    "project")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name", "budget", "status")


admin.site.register(Team)
admin.site.register(Position)
admin.site.register(TaskType)
