from typing import Any, Dict, List, Optional

from src.database.Database import Database
from src.tasks.exceptions import TaskAlreadyExists, UserNotFound
from src.tasks.schemas import AddTask, AddTaskResponse


class Tasks:
    """
    Tasks handler

    Methods
    -------
    add_task(AddTaskRequest: AddTask) -> AddTaskResponse
        Add task
    _get_user_by_email(email: str) -> Optional[Dict[str, str]]
        Get user by email
    _get_user_tasks(user: Dict[str, str]) -> Optional[List[Dict[str, str]]]
        Get user tasks
    """

    def __init__(self):
        """
        Initialize tasks handler
        """

        self.client = Database().get_client()
        self.users = self.client["task-manager-db"]["users"]

    def add_task(self, AddTaskRequest: AddTask) -> AddTaskResponse:
        """

        Parameters
        ----------
        AddTaskRequest : AddTask
            The request body

        Returns
        -------
        AddTaskResponse
            The response body
        """

        user = self._get_user_by_email(AddTaskRequest.email)
        new_task = AddTaskRequest.task

        if not user:
            raise UserNotFound()

        tasks = self._get_user_tasks(user=user)

        if not tasks:
            tasks = []

        for task in tasks:
            if task["title"] == new_task.title:
                raise TaskAlreadyExists()

        tasks.append(new_task.__dict__)

        self.users.update_one(
            {"email": AddTaskRequest.email}, {"$set": {"tasks": tasks}}
        )

        return AddTaskResponse(detail="Task added successfully")

    def _get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email

        Parameters
        ----------
        email : str
            User email

        Returns
        -------
        Optional[Dict[str, Any]]
            User data
        """

        return self.users.find_one({"email": email})

    def _get_user_tasks(self, user: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
        """
        Get user tasks

        Parameters
        ----------
        user : Dict[str, Any]
            User data

        Returns
        -------
        Optional[Dict[str, str]]
            User tasks
        """

        return user.get("tasks")
