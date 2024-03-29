from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    deadline: datetime


class GetTasksResponse(BaseModel):
    tasks: List[Task]


class AddTask(BaseModel):
    email: str
    task: Task


class AddTaskResponse(BaseModel):
    detail: str
