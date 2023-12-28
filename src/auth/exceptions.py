from fastapi import HTTPException


class SignInWrongCredentials(HTTPException):
    """
    Exception that is raised when
    user enters wrong credentials
    """

    def __init__(self):
        """
        Initialize exception
        """

        super().__init__(status_code=401, detail="Incorrect email or password")


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


class SecretNotProvided(Exception):
    """
    Exception that is raised
    when secret is not provided
    """

    pass
