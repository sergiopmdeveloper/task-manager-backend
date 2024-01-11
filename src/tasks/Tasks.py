from typing import Any, Dict, List, Optional

from src.database.Database import Database
from src.tasks.exceptions import TaskAlreadyExists, UserNotFound
from src.tasks.schemas import AddTask, AddTaskResponse, GetTasksResponse


class Tasks:
    """
    Tasks handler

    Methods
    -------
    get_tasks(email: str) -> GetTasksResponse
        Get a user's list of tasks
    add_task(add_task_request: AddTask) -> AddTaskResponse
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

    def get_tasks(self, email: str) -> GetTasksResponse:
        """
        Get a user's list of tasks

        Parameters
        ----------
        email : str
            The user's email

        Returns
        -------
        GetTasksResponse
            The response body

        Raises
        ------
        UserNotFound
            If the user is not found
        """

        user = self._get_user_by_email(email)

        if not user:
            raise UserNotFound()

        tasks = self._get_user_tasks(user=user)

        if not tasks:
            tasks = []

        return GetTasksResponse(tasks=tasks)

    def add_task(self, add_task_request: AddTask) -> AddTaskResponse:
        """
        Add task to a user's list of tasks

        Parameters
        ----------
        add_task_request : AddTask
            The request body

        Returns
        -------
        AddTaskResponse
            The response body

        Raises
        ------
        UserNotFound
            If the user is not found
        TaskAlreadyExists
            If the task already exists
        """

        user = self._get_user_by_email(add_task_request.email)
        new_task = add_task_request.task

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
            {"email": add_task_request.email}, {"$set": {"tasks": tasks}}
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
