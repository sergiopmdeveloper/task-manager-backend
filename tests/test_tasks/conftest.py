from typing import Dict, List
from unittest.mock import patch

import pytest
from pytest import MonkeyPatch

from src.tasks.schemas import AddTask, AddTaskResponse, Task
from src.tasks.Tasks import Tasks


@pytest.fixture
def fake_add_task() -> AddTask:
    """
    Returns an AddTask instance

    Returns
    -------
    AddTask
        AddTask instance
    """

    return AddTask(
        email="fake_email",
        task=Task(
            title="fake_title",
            description="fake_description",
            status="fake_status",
            priority="fake_priority",
            deadline="fake_deadline",
        ),
    )


@pytest.fixture
def fake_user_tasks_existing_task() -> List[Dict[str, str]]:
    """
    Returns a list with a task that already exists

    Returns
    -------
    List[Dict[str, str]]
        List with a task
    """

    return [
        {
            "title": "fake_title",
            "description": "fake_description",
            "status": "fake_status",
            "priority": "fake_priority",
            "deadline": "fake_deadline",
        }
    ]


@pytest.fixture
def fake_user_tasks_not_existing_task() -> List[Dict[str, str]]:
    """
    Returns a list with a task that does not exist

    Returns
    -------
    List[Dict[str, str]]
        List with a task
    """

    return [
        {
            "title": "fake_title_different",
            "description": "fake_description_different",
            "status": "fake_status_different",
            "priority": "fake_priority_different",
            "deadline": "fake_deadline_different",
        }
    ]


@pytest.fixture
def fake_add_task_response() -> AddTaskResponse:
    """
    Returns an AddTaskResponse instance

    Returns
    -------
    AddTaskResponse
        AddTaskResponse instance
    """

    return AddTaskResponse(
        detail="Task added successfully",
    )


@pytest.fixture
def tasks(monkeypatch: MonkeyPatch) -> Tasks:
    """
    Returns a Tasks instance

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items

    Returns
    -------
    Tasks
        Tasks instance
    """

    monkeypatch.setenv("JWT_SECRET_KEY", "fake_jwt_secret_key")

    with patch("src.auth.Auth.Database.get_client"):
        tasks = Tasks()

    return tasks
