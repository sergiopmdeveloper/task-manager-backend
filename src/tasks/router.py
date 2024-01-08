from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.router import oauth2_scheme
from src.auth.utils import verify_access_token
from src.tasks.schemas import AddTask, AddTaskResponse
from src.tasks.Tasks import Tasks

tasks_router = APIRouter(prefix="/tasks")


def get_tasks() -> Tasks:
    """
    Get tasks handler

    Returns
    -------
    Tasks
        The tasks handler
    """

    return Tasks()


@tasks_router.post(
    "/add_task", status_code=status.HTTP_201_CREATED, response_model=AddTaskResponse
)
def add_task(
    AddTaskRequest: AddTask,
    token: Annotated[str, Depends(oauth2_scheme)],
    tasks: Tasks = Depends(get_tasks),
) -> AddTaskResponse:
    """
    Add a task to a user's list of tasks

    Parameters
    ----------
    AddTaskRequest : AddTask
        The request body
    token : Annotated[str, Depends(oauth2_scheme)]
        The access token

    Returns
    -------
    AddTaskResponse
        The response body
    """

    verify_access_token(token=token)

    tasks.add_task(add_task_request=AddTaskRequest)

    return AddTaskResponse(detail="Task added successfully")
