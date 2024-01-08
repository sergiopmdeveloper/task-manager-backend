from fastapi.exceptions import HTTPException


class UserNotFound(HTTPException):
    """
    Exception that is raised
    when user is not found
    """

    def __init__(self):
        """
        Initialize exception
        """

        super().__init__(
            status_code=404,
            detail="User not found",
        )


class TaskAlreadyExists(HTTPException):
    """
    Exception that is raised
    when task already exists
    """

    def __init__(self):
        """
        Initialize exception
        """

        super().__init__(
            status_code=409,
            detail="Task already exists",
        )
