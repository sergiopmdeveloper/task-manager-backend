import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from src.auth.Auth import Auth
from src.auth.exceptions import UserAlreadyExists
from src.auth.schemas import SignUpResponse, User
from src.auth.utils import (
    JWT_ALGORITHM,
    create_access_token,
    get_password_hash,
)
from src.main import app

client = TestClient(app)

fake_user = User(name="fake_name", email="fake_email", password="fake_password")
fake_response = SignUpResponse(user_id="fake_user_id", access_token="fake_access_token")


@pytest.fixture
def auth() -> Auth:
    """
    Returns an Auth instance

    Returns
    -------
    Auth
        Auth instance
    """

    os.environ["JWT_SECRET_KEY"] = "fake_jwt_secret_key"

    with patch("src.auth.Auth.Database.get_client"):
        auth = Auth()

    return auth


def test_auth_get_password_hash() -> None:
    """
    Test the get_password_hash function
    """

    password_hash = get_password_hash(password=fake_user.password.get_secret_value())

    assert fake_user.password != password_hash
    assert isinstance(password_hash, str)


def test_auth_create_access_token() -> None:
    """
    Test the create_access_token function
    """

    os.environ["JWT_SECRET_KEY"] = "fake_jwt_secret_key"

    access_token = create_access_token()

    decoded_access_token = jwt.decode(
        access_token, os.environ["JWT_SECRET_KEY"], algorithms=[JWT_ALGORITHM]
    )

    assert ["iat", "exp"] == list(decoded_access_token.keys())


def test_auth_get_user_by_email_find_one_called(auth: Auth) -> None:
    """
    Test if find_one method is called
    in _get_user_by_email method

    Parameters
    ----------
    auth : Auth
        Auth instance
    """

    auth._get_user_by_email(email=fake_user.email)

    auth.users.find_one.assert_called_once_with({"email": fake_user.email})


def test_auth_sign_up_insert_one_called(auth: Auth) -> None:
    """
    Test if insert_one method
    is called in sign_up method

    Parameters
    ----------
    auth : Auth
        Auth instance
    """

    auth.users.find_one.return_value = None

    auth.sign_up(user=fake_user)

    auth.users.insert_one.assert_called_once()


def test_auth_sign_up_returns_response(auth: Auth) -> None:
    """
    Test if sign_up method returns the expected response

    Parameters
    ----------
    auth : Auth
        Auth instance
    """

    auth.users.find_one.return_value = None
    auth.users.insert_one.return_value.inserted_id = fake_response.user_id

    response = auth.sign_up(user=fake_user)

    assert ["user_id", "access_token"] == list(response.__dict__.keys())
    assert response.user_id == fake_response.user_id
    assert isinstance(response.access_token, str)


def test_auth_sign_up_user_already_exists(auth: Auth) -> None:
    """
    Test if UserAlreadyExists exception
    is raised when user already exists

    Parameters
    ----------
    auth : Auth
        Auth instance
    """

    auth.users.find_one.return_value = fake_user

    with pytest.raises(UserAlreadyExists):
        auth.sign_up(user=fake_user)


def test_auth_sign_up_route_201() -> None:
    """
    Test the sign_up route with status code 201
    """

    with patch("src.auth.router.Auth") as auth_mock:
        auth_mock.return_value.sign_up.return_value = fake_response

        fake_user_dict = fake_user.__dict__
        fake_user_dict["password"] = fake_user_dict["password"].get_secret_value()

        response = client.post("/auth/sign-up", json=fake_user_dict)

    assert response.status_code == 201
    assert response.json() == fake_response.__dict__
