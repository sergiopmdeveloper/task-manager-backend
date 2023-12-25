from typing import Dict

from fastapi import APIRouter, status

from src.auth.Auth import Auth
from src.auth.schemas import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED)
def sign_up(user: User) -> Dict[str, str]:
    """
    Sign up user

    Parameters
    ----------
    user : User
        User data

    Returns
    -------
    Dict[str, str]
        Response detail
    """

    response = Auth().sign_up(user=user)

    return response
