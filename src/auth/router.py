from fastapi import APIRouter, Depends, status

from src.auth.Auth import Auth
from src.auth.schemas import SignUpResponse, User

auth_router = APIRouter(prefix="/auth")


def get_auth() -> Auth:
    """
    Returns an Auth instance

    Returns
    -------
    Auth
        Auth instance
    """

    return Auth()


@auth_router.post(
    "/sign-up", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse
)
def sign_up(user: User, auth: Auth = Depends(get_auth)) -> SignUpResponse:
    """
    Sign up user

    Parameters
    ----------
    user : User
        User data
    auth : Auth
        Auth instance

    Returns
    -------
    SignUpResponse
        Response detail
    """

    return auth.sign_up(user=user)
