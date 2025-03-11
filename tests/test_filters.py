from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, TaskType, Project, Task


PROJECT_LIST_URL = reverse("task_manager:project-list")
TASK_LIST_URL = reverse("task_manager:task-list")


class TestTaskListFilters(TestCase):
    def setUp(self) -> None:
        username = "test"
        password = "test123"
        self.position = Position.objects.create(name="test_position")

        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position,
        )
        self.client.force_login(self.user)

        self.task_type_1 = TaskType.objects.create(name="test_type_1")
        self.task_type_2 = TaskType.objects.create(name="test_type_2")

        self.project = Project.objects.create(
            project_name="test_project", deadline="2025-01-01", status="Active"
        )

        date_now = datetime.now().date()

        self.task_1 = Task.objects.create(
            name="test_type_1",
            deadline=date_now + timedelta(days=1),
            is_completed=False,
            task_type=self.task_type_1,
            project=self.project
        )
        self.task_1.assignees.set([self.user])
        self.task_2 = Task.objects.create(
            name="test_type_2",
            deadline=date_now + timedelta(days=1),
            is_completed=True,
            task_type=self.task_type_2,
            project=self.project
        )
        self.task_2.assignees.set([self.user])
        self.task_3 = Task.objects.create(
            name="test_type_3",
            deadline=date_now - timedelta(days=1),
            is_completed=False,
            task_type=self.task_type_1,
            project=self.project
        )
        self.task_3.assignees.set([self.user])

    def test_filter_overdue_tasks(self) -> None:
        response = self.client.get(TASK_LIST_URL + "?overdue=true")
        self.assertEqual(len(response.context_data["task_list"]), 1)
        self.assertIn(self.task_3, response.context_data["task_list"])

    def test_filter_hide_completed_tasks(self) -> None:
        response = self.client.get(TASK_LIST_URL + "?hide_completed=true")
        self.assertEqual(len(response.context_data["task_list"]), 2)
        self.assertIn(self.task_1, response.context_data["task_list"])
        self.assertIn(self.task_3, response.context_data["task_list"])

    def test_filter_by_task_type(self) -> None:
        response = self.client.get(
            TASK_LIST_URL + f"?{self.task_type_1.name}=true")
        self.assertEqual(len(response.context_data["task_list"]), 2)
        self.assertIn(self.task_1, response.context_data["task_list"])
        self.assertIn(self.task_3, response.context_data["task_list"])

    def test_filter_combined(self) -> None:
        response = self.client.get(
            TASK_LIST_URL +
            f"?overdue=true&hide_completed=true&{self.task_type_1.name}=true"
        )
        self.assertEqual(len(response.context_data["task_list"]), 1)
        self.assertIn(self.task_3, response.context_data["task_list"])


class TestProjectListFilters(TestCase):
    def setUp(self) -> None:
        username = "test"
        password = "test123"
        self.position = Position.objects.create(name="test_position")

        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position,
        )
        self.client.force_login(self.user)

        date_now = datetime.now().date()

        self.project_1 = Project.objects.create(
            project_name="test_project_1",
            deadline=date_now + timedelta(days=1),
            status="Active",
        )
        self.project_2 = Project.objects.create(
            project_name="test_project_2",
            deadline=date_now - timedelta(days=1),
            status="Active",
        )
        self.project_3 = Project.objects.create(
            project_name="test_project_3",
            deadline=date_now + timedelta(days=1),
            status="Completed",
        )

    def test_filter_overdue_project(self) -> None:
        response = self.client.get(PROJECT_LIST_URL + "?overdue=true")
        self.assertEqual(len(response.context_data["project_list"]), 1)
        self.assertIn(self.project_2, response.context_data["project_list"])

    def test_filter_active_project(self) -> None:
        response = self.client.get(PROJECT_LIST_URL + "?active=true")
        self.assertEqual(len(response.context_data["project_list"]), 2)
        self.assertIn(self.project_1, response.context_data["project_list"])
        self.assertIn(self.project_2, response.context_data["project_list"])
