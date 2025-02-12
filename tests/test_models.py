from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import (TaskType,
                                 Position,
                                 Task,
                                 Project,
                                 Team)


class ModelsTests(TestCase):
    def test_task_type_str(self) -> None:
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type),
                         f"{task_type.name}")


    def test_task_type_ordering(self) -> None:
        task_type_last = TaskType.objects.create(name="c_test")
        task_type_middle = TaskType.objects.create(name="b_test")
        task_type_first = TaskType.objects.create(name="a_test")

        list_task_type= [task_type_first, task_type_middle, task_type_last]
        self.assertEqual(list_task_type,
                         list(TaskType.objects.all()))

    def test_position_str(self) -> None:
        position = Position.objects.create(name="test")
        self.assertEqual(str(position),
                         f"{position.name}")

    def test_position_ordering(self) -> None:
        position_last = Position.objects.create(name="c_test")
        position_middle = Position.objects.create(name="b_test")
        position_first = Position.objects.create(name="a_test")

        list_positions= [position_first, position_middle, position_last]
        self.assertEqual(list_positions,
                         list(Position.objects.all()))

    def test_task_str(self) -> None:
        task_type = TaskType.objects.create(name="test")
        position = Position.objects.create(name="test")
        assign = get_user_model().objects.create(
                    username="test",
                    password="test123",
                    first_name="test_first",
                    last_name="test_last",
                    position=position)
        task = Task.objects.create(name="test",
                                   description="test description",
                                   deadline="2025-01-01",
                                   is_completed=True,
                                   priority="High",
                                   task_type=task_type)

        task.assignees.set([assign])

        workers = ", ".join([str(worker) for worker in task.assignees.all()])

        self.assertEqual(str(task),
                         f"{task.name}: Completed! Workers: {workers}")

        task.is_completed = False

        self.assertEqual(str(task),
                         f"{task.name}: Not Completed! "
                        f"Priority: {task.priority}, "
                        f"Deadline={task.deadline}, "
                        f"Workers: {workers}")

    def test_project_str(self) -> None:
        project = Project.objects.create(project_name="test",
                                         deadline="2025-01-01",
                                         status = "Active")

        self.assertEqual(str(project),
                         f"{project.project_name}, status: {project.status}")


    def test_team_str(self) -> None:
        team = Team.objects.create(name="test")

        self.assertEqual(str(team),
                         team.name)

    def test_driver_str(self) -> None:
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="text_last",
            position=position
        )
        self.assertEqual(str(worker),
                         f"{worker.username}: "
                         f"({worker.first_name} {worker.last_name})"
                         f"Position: {worker.position.name}")



class CustomFieldsTests(TestCase):
    def test_create_driver_with_licence_number(self):
        username = "test"
        password = "test123"
        position = Position.objects.create(name="test_position")
        team = Team.objects.create(name="test_team")
        is_team_lead = True

        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
            team=team,
            is_team_lead=is_team_lead
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position, position)
        self.assertEqual(worker.team, team)
        self.assertEqual(worker.is_team_lead, is_team_lead)
        self.assertTrue(worker.check_password(password))
