from fastapi import HTTPException


class UserAlreadyExists(HTTPException):
    """
    Exception that is raised
    when user already exists
    """

    def __init__(self):
        """
        Initialize exception
        """

        super().__init__(
            status_code=409,
            detail="User already exists",
        )
