from django.contrib.auth import get_user_model
from django.forms import forms
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import TaskForm
from task_manager.models import Project, Task, Team, Position, TaskType


WORKER_LIST_URL = reverse("task_manager:worker-list")
PROJECT_LIST_URL = reverse("task_manager:project-list")
TASK_LIST_URL = reverse("task_manager:task-list")
TEAM_LIST_URL = reverse("task_manager:team-list")


class PublicAccessTests(TestCase):
    def test_worker_login_required(self):
        res = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_project_login_required(self):
        res = self.client.get(PROJECT_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_login_required(self):
        res = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_team_login_required(self):
        res = self.client.get(TEAM_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateAccessTests(TestCase):
    def setUp(self):
        username = "test"
        password = "test123"
        self.position = Position.objects.create(name="test_position")
        team = Team.objects.create(name="test_team")
        is_team_lead = True

        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position,
            team=team,
            is_team_lead=is_team_lead
        )

        self.client.force_login(self.user)

    def test_retrieve_projects(self):
        Project.objects.create(project_name="test1",
                               deadline="2025-01-01",
                               status="Active")
        Project.objects.create(project_name="test2",
                               deadline="2025-01-01",
                               status="Active")
        response = self.client.get(PROJECT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        projects = Project.objects.all()
        self.assertEqual(
            list(response.context["project_list"]),
            list(projects)
        )
        self.assertTemplateUsed(response, "task_manager/project_list.html")

    def test_retrieve_tasks(self):
        task_type = TaskType.objects.create(name="test")

        task_1 = Task.objects.create(
            name="test_1",
            description="test description",
            deadline="2025-01-01",
            is_completed=True,
            priority=1,
            task_type=task_type)
        task_1.assignees.set([self.user])

        task_2 = Task.objects.create(
            name="test_2",
            description="test description",
            deadline="2025-01-01",
            is_completed=True,
            priority=1,
            task_type=task_type)
        task_2.assignees.set([self.user])

        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_retrieve_team(self):
        project = Project.objects.create(
            project_name="test2",
            deadline="2025-01-01",
            status="Active")

        Team.objects.create(name="test_1", project=project)
        Team.objects.create(name="test_2", project=project)

        response = self.client.get(TEAM_LIST_URL)
        self.assertEqual(response.status_code, 200)
        teams = Team.objects.all()
        self.assertEqual(
            list(response.context["team_list"]),
            list(teams)
        )
        self.assertTemplateUsed(response, "task_manager/team_list.html")

    def test_retrieve_worker(self):
        password = "test123"

        get_user_model().objects.create_user(
            username="test_1",
            password=password,
            position=self.position
        )

        get_user_model().objects.create_user(
            username="test_2",
            password=password,
            position=self.position
        )

        response = self.client.get(WORKER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        workers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")


class CreateTest(TestCase):
    def setUp(self):
        username = "test"
        password = "test123"
        self.position = Position.objects.create(name="test_position")
        team = Team.objects.create(name="test_team")
        is_team_lead = True

        self.project = Project.objects.create(
            project_name="test",
            deadline="2025-01-01",
            status="Active")

        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position,
            team=team,
            is_team_lead=is_team_lead
        )
        self.client.force_login(self.user)

    def test_create_worker(self):
        team = Team.objects.create(name="test_team")
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": self.position.pk,
            "team": team.pk,
            "is_team_lead": True
        }

        response = self.client.post(
            reverse("task_manager:worker-create"), data=form_data)
        print(response.status_code)
        print(response.content)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position.pk, form_data["position"])


    def test_task_create_from_worker_page_with_worker(self):
        url = reverse("task_manager:task-create")
        response = self.client.get(url, {"worker_id": self.user.id})

        print(response.context)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertIsInstance(form, TaskForm)
        self.assertEqual(list(form.initial.get("assignees", [])), [self.user])


    def test_task_create_from_project_page_with_project(self):
        url = reverse("task_manager:task-create")
        response = self.client.get(url, {"project_id": self.project.id})

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertIsInstance(form, TaskForm)
        self.assertEqual(form.initial.get("project"), self.project)


class SetTaskAsCompletedTest(TestCase):
    def setUp(self):
        username = "test"
        password = "test123"
        self.position = Position.objects.create(name="test_position")

        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position,
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(name="test_type")
        self.project = Project.objects.create(project_name="test_project",
                                              deadline="2025-01-01",
                                              status="Active")

        self.task = Task.objects.create(name="test_1",
                                        description="test description",
                                        deadline="2025-01-01",
                                        is_completed=False,
                                        priority=1,
                                        task_type=self.task_type,
                                        project=self.project)
        self.task.assignees.set([self.user])
        self.url = reverse("task_manager:task-detail", args=[self.task.pk])

    def test_setup_task_as_completed(self):
        response = self.client.post(
            reverse("task_manager:set-task-as-completed", args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertEqual(self.task.is_completed, True)
        self.assertRedirects(response, self.url)
