from typing import Dict, List
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.tasks.exceptions import UserNotFound
from src.tasks.schemas import GetTasksResponse
from src.tasks.Tasks import Tasks

client = TestClient(app)


def test_get_tasks_user_not_found(tasks: Tasks) -> None:
    """
    Test that get_tasks raises UserNotFound when the user is not found

    Parameters
    ----------
    tasks : Tasks
        The tasks instance
    """

    tasks.users.find_one.return_value = None

    with pytest.raises(UserNotFound):
        tasks.get_tasks(email="fake_email")


def test_get_tasks_response(tasks: Tasks, fake_tasks: List[Dict[str, str]]) -> None:
    """
    Test that get_tasks returns the correct response

    Parameters
    ----------
    tasks : Tasks
        The tasks instance
    fake_tasks : List[Dict[str, str]]
        The fake tasks
    """

    tasks.users.find_one.return_value = {"tasks": fake_tasks}

    assert tasks.get_tasks(email="fake_email") == GetTasksResponse(tasks=fake_tasks)


def test_tasks_get_tasks_route_200(fake_tasks: List[Dict[str, str]]) -> None:
    """
    Test that the route /tasks/get-tasks returns 200

    Parameters
    ----------

    fake_tasks : List[Dict[str, str]]
        The fake tasks
    """

    with (
        patch("src.tasks.router.Tasks") as tasks_mock,
        patch("src.tasks.router.verify_access_token") as verify_access_token_mock,
    ):
        tasks_mock.return_value.get_tasks.return_value = GetTasksResponse(
            tasks=fake_tasks
        )
        verify_access_token_mock.return_value = True

        fake_tasks[0]["deadline"] = fake_tasks[0]["deadline"].isoformat()

        response = client.get(
            "/tasks/get-tasks",
            params={"email": "fake_email"},
            headers={"Authorization": "Bearer fake_token"},
        )

    assert response.status_code == 200
    assert response.json()["tasks"] == fake_tasks
