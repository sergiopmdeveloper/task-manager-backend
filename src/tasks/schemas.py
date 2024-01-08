from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    deadline: str


class AddTask(BaseModel):
    email: str
    task: Task


class AddTaskResponse(BaseModel):
    detail: str
