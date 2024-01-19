from typing import Dict, List
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.tasks.exceptions import TaskAlreadyExists, UserNotFound
from src.tasks.schemas import AddTask, AddTaskResponse
from src.tasks.Tasks import Tasks

client = TestClient(app)


def test_add_task_user_not_found(tasks: Tasks, fake_add_task: AddTask) -> None:
    """
    Test add_task method when user is not found

    Parameters
    ----------
    tasks : Tasks
        Tasks instance
    fake_add_task : AddTask
        AddTask instance
    """

    tasks.users.find_one.return_value = None

    with pytest.raises(UserNotFound):
        tasks.add_task(add_task_request=fake_add_task)


def test_add_task_task_already_exists(
    tasks: Tasks,
    fake_add_task: AddTask,
    fake_user_tasks_existing_task: List[Dict[str, str]],
) -> None:
    """
    Test add_task method when task already exists

    Parameters
    ----------
    tasks : Tasks
        Tasks instance
    fake_add_task : AddTask
        AddTask instance
    fake_user_tasks_existing_task : List[Dict[str, str]]
        List with a task
    """

    tasks.users.find_one.return_value = {
        "_id": "fake_id",
        "name": "fake_name",
        "email": "fake_email",
        "password": "fake_password",
        "tasks": fake_user_tasks_existing_task,
    }

    with pytest.raises(TaskAlreadyExists):
        tasks.add_task(add_task_request=fake_add_task)


def test_add_task_new_task(
    tasks: Tasks,
    fake_add_task: AddTask,
    fake_user_tasks_not_existing_task: List[Dict[str, str]],
) -> None:
    """
    Test add_task method when task is new

    Parameters
    ----------
    tasks : Tasks
        Tasks instance
    fake_add_task : AddTask
        AddTask instance
    fake_user_tasks_not_existing_task : List[Dict[str, str]]
        List with a task
    """

    tasks.users.find_one.return_value = {
        "_id": "fake_id",
        "name": "fake_name",
        "email": "fake_email",
        "password": "fake_password",
        "tasks": fake_user_tasks_not_existing_task,
    }

    tasks.add_task(add_task_request=fake_add_task)

    tasks.users.update_one.assert_called_once()


def test_tasks_add_task_route_201(
    fake_add_task_response: AddTaskResponse, fake_add_task: AddTask
) -> None:
    """
    Test /tasks/add-task route when status code is 201

    Parameters
    ----------
    fake_add_task_response : AddTaskResponse
        AddTaskResponse instance
    fake_add_task : AddTask
        AddTask instance
    """

    with (
        patch("src.tasks.router.Tasks") as tasks_mock,
        patch("src.tasks.router.verify_access_token") as verify_access_token_mock,
    ):
        tasks_mock.return_value.add_task.return_value = fake_add_task_response
        verify_access_token_mock.return_value = True

        fake_add_task_dict = fake_add_task.__dict__
        fake_add_task_dict["task"] = fake_add_task_dict["task"].__dict__
        fake_add_task_dict["task"]["deadline"] = str(
            fake_add_task_dict["task"]["deadline"]
        )

        response = client.post(
            "/tasks/add-task",
            json=fake_add_task_dict,
            headers={"Authorization": "Bearer fake_token"},
        )

    assert response.status_code == 201
    assert response.json() == fake_add_task_response.__dict__
