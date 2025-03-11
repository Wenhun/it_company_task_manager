from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Team, Position, Task, TaskType, Project

FIRST_SEARCH_LETTER = "J"

TEST_PASSWORD = "test123"


class SearchTests:
    model: TestCase
    object_1: str
    object_2: str
    object_3: str
    url: str

    @staticmethod
    def create_user() -> AbstractBaseUser:
        username = "test"

        position = Position.objects.create(name="test_position")
        team = Team.objects.create(name="test_team")
        is_team_lead = True

        user = get_user_model().objects.create_user(
            username=username,
            password=TEST_PASSWORD,
            position=position,
            team=team,
            is_team_lead=is_team_lead
        )

        return user

    def test_empty_search_return_all(self) -> None:
        response = self.model.client.get(self.url)
        self.model.assertEqual(response.status_code, 200)
        self.model.assertContains(response, self.object_1)
        self.model.assertContains(response, self.object_2)
        self.model.assertContains(response, self.object_3)

    def test_search_work_with_part_of_request(self) -> None:
        response = self.client.get(
            self.url, {
                "search_field":
                    self.object_1[:len(FIRST_SEARCH_LETTER)]})
        self.model.assertEqual(response.status_code, 200)
        self.model.assertContains(response,  self.object_1)
        self.model.assertContains(response, self.object_2)
        self.model.assertNotContains(response, self.object_3)

    def test_search_not_found_nothing_return_empty_list(self) -> None:
        response = self.model.client.get(self.url, {"search_field": "123aaa"})
        self.model.assertEqual(response.status_code, 200)
        self.model.assertNotContains(response, self.object_1)
        self.model.assertNotContains(response, self.object_2)
        self.model.assertNotContains(response, self.object_3)

    def test_search_case_insensitive(self) -> None:
        response = self.model.client.get(
            self.url,
            {"search_field": self.object_1.upper()})
        self.model.assertEqual(response.status_code, 200)
        self.model.assertContains(response, self.object_1)
        self.model.assertNotContains(response, self.object_2)
        self.model.assertNotContains(response, self.object_3)


class WorkerSearchTests(TestCase, SearchTests):
    def setUp(self) -> None:
        user = self.create_user()
        self.client.force_login(user)

        worker_1 = get_user_model().objects.create(
            username=FIRST_SEARCH_LETTER + "ohn Test",
            password=TEST_PASSWORD,
            position=user.position)
        worker_2 = get_user_model().objects.create(
            username=FIRST_SEARCH_LETTER + "ane Test",
            password=TEST_PASSWORD,
            position=user.position)
        worker_3 = get_user_model().objects.create(
            username="Bob Test",
            password=TEST_PASSWORD,
            position=user.position)

        self.model = self
        self.object_1 = worker_1.get_username()
        self.object_2 = worker_2.get_username()
        self.object_3 = worker_3.get_username()
        self.url = reverse("task_manager:worker-list")


class TaskSearchTests(TestCase, SearchTests):
    def setUp(self) -> None:
        user = self.create_user()
        self.client.force_login(user)

        task_type = TaskType.objects.create(name="test_type")
        project = Project.objects.create(
            project_name="test_project",
            deadline="2025-01-01",
            status="Active")

        task_1 = Task.objects.create(
            name=FIRST_SEARCH_LETTER + "ust",
            description="test_description",
            deadline="2025-01-01",
            is_completed=False,
            priority=1,
            task_type=task_type,
            project=project)
        task_1.assignees.set([user])
        task_2 = Task.objects.create(
            name=FIRST_SEARCH_LETTER + "ob",
            description="test_description",
            deadline="2025-01-01",
            is_completed=False,
            priority=1,
            task_type=task_type,
            project=project)
        task_2.assignees.set([user])
        task_3 = Task.objects.create(
            name="Fix",
            description="test_description",
            deadline="2025-01-01",
            is_completed=False,
            priority=1,
            task_type=task_type,
            project=project)
        task_3.assignees.set([user])

        self.model = self
        self.object_1 = task_1.name
        self.object_2 = task_2.name
        self.object_3 = task_3.name
        self.url = reverse("task_manager:task-list")


class ProjectSearchTests(TestCase, SearchTests):
    def setUp(self) -> None:
        user = self.create_user()
        self.client.force_login(user)

        project_1 = Project.objects.create(
            project_name=FIRST_SEARCH_LETTER + "ust",
            deadline="2025-01-01",
            status="Active")

        project_2 = Project.objects.create(
            project_name=FIRST_SEARCH_LETTER + "ob",
            deadline="2025-01-01",
            status="Active")

        project_3 = Project.objects.create(
            project_name="noname",
            deadline="2025-01-01",
            status="Active")

        self.model = self
        self.object_1 = project_1.project_name
        self.object_2 = project_2.project_name
        self.object_3 = project_3.project_name
        self.url = reverse("task_manager:project-list")
