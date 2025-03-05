from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position, Team


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position.objects.create(name="test_position")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
            position=position
        )
        self.client.force_login(self.admin_user)
        team = Team.objects.create(name="test_team")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=position,
            team=team,
            is_team_lead=False
        )

    def test_worker_custom_fields_listed(self) -> None:
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)
        self.assertContains(res, self.worker.team)
        self.assertContains(res, self.worker.is_team_lead)

    def test_worker_detail_custom_fields_listed(self) -> None:
        url = reverse("admin:task_manager_worker_change",
                      args=[self.worker.id])
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)
        self.assertContains(res, self.worker.team)
