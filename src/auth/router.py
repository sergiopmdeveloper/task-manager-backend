from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.Auth import Auth
from src.auth.schemas import AuthResponse, UserSignIn, UserSignUp, VerifyTokenResponse
from src.auth.utils import verify_access_token

auth_router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth() -> Auth:
    """
    Returns an Auth instance

    Returns
    -------
    Auth
        Auth instance
    """

    return Auth()


@auth_router.post("/token", status_code=status.HTTP_200_OK, response_model=AuthResponse)
def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(), auth: Auth = Depends(get_auth)
) -> AuthResponse:
    """
    Sign in user and email and token

    Parameters
    ----------
    form_data : OAuth2PasswordRequestForm
        Form data with username (email) and password
    auth : Auth
        Auth instance

    Returns
    -------
    AuthResponse
        Response detail
    """

    user = UserSignIn(email=form_data.username, password=form_data.password)

    return auth.sign_in(user=user)


@auth_router.post(
    "/sign-up", status_code=status.HTTP_201_CREATED, response_model=AuthResponse
)
def sign_up(user: UserSignUp, auth: Auth = Depends(get_auth)) -> AuthResponse:
    """
    Sign up user

    Parameters
    ----------
    user : UserSignUp
        User data
    auth : Auth
        Auth instance

    Returns
    -------
    AuthResponse
        Response detail
    """

    return auth.sign_up(user=user)


@auth_router.post("/verify-token", status_code=status.HTTP_200_OK)
def verify_token(token: str) -> VerifyTokenResponse:
    """
    Verify access token

    Parameters
    ----------
    token : str
        Access token

    Returns
    -------
    VerifyTokenResponse
        Response detail
    """

    verify_access_token(token=token)

    return VerifyTokenResponse(detail="Token is valid")
