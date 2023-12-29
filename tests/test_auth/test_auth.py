import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from pytest import MonkeyPatch

from src.auth.Auth import Auth
from src.auth.exceptions import (
    SecretNotProvided,
    SignInWrongCredentials,
    TokenVerificationError,
    UserAlreadyExists,
)
from src.auth.schemas import AuthResponse, UserSignIn, UserSignUp
from src.auth.utils import (
    JWT_ALGORITHM,
    create_access_token,
    get_password_hash,
    verify_access_token,
    verify_password,
)
from src.main import app
from tests.test_auth.types import FakeFindOneResponse

client = TestClient(app)


def test_auth_get_password_hash(fake_user_sign_up: UserSignUp) -> None:
    """
    Test the get_password_hash function

    Parameters
    ----------
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    password_hash = get_password_hash(
        password=fake_user_sign_up.password.get_secret_value()
    )

    assert fake_user_sign_up.password != password_hash
    assert isinstance(password_hash, str)


def test_auth_verify_password(fake_user_sign_up: UserSignUp) -> None:
    """
    Test the verify_password function

    Parameters
    ----------
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    password = fake_user_sign_up.password.get_secret_value()
    password_hash = get_password_hash(password=password)

    assert verify_password(
        plain_password=password,
        hashed_password=password_hash,
    )


def test_auth_create_access_token_secret_not_provided(monkeypatch: MonkeyPatch) -> None:
    """
    Test the create_access_token function

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items
    """

    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(SecretNotProvided):
        create_access_token()


def test_auth_create_access_token_success(monkeypatch: MonkeyPatch) -> None:
    """
    Test the create_access_token function

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items
    """

    monkeypatch.setenv("JWT_SECRET_KEY", "fake_jwt_secret_key")

    access_token = create_access_token()

    decoded_access_token = jwt.decode(
        access_token, os.getenv("JWT_SECRET_KEY"), algorithms=[JWT_ALGORITHM]
    )

    assert isinstance(access_token, str)
    assert ["iat", "exp"] == list(decoded_access_token.keys())


def test_auth_verify_access_token_secret_not_provided(monkeypatch: MonkeyPatch) -> None:
    """
    Test the verify_access_token function

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items
    """

    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(SecretNotProvided):
        verify_access_token(token="fake_token")


def test_auth_verify_access_token_failed(monkeypatch: MonkeyPatch) -> None:
    """
    Test the verify_access_token function

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items
    """

    monkeypatch.setenv("JWT_SECRET_KEY", "fake_jwt_secret_key")

    with pytest.raises(TokenVerificationError):
        verify_access_token(token="fake_token")


def test_auth_verify_access_token_success(monkeypatch: MonkeyPatch) -> None:
    """
    Test the verify_access_token function

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items
    """

    monkeypatch.setenv("JWT_SECRET_KEY", "fake_jwt_secret_key")

    access_token = create_access_token()

    assert verify_access_token(token=access_token)


def test_auth_get_user_by_email_find_one_called(
    auth: Auth, fake_user_sign_up: UserSignUp
) -> None:
    """
    Test if find_one method is called
    in _get_user_by_email method

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    auth._get_user_by_email(email=fake_user_sign_up.email)

    auth.users.find_one.assert_called_once_with({"email": fake_user_sign_up.email})


def test_auth_sign_in_user_not_found(auth: Auth, fake_user_sign_in: UserSignIn) -> None:
    """
    Test if UserNotFound exception
    is raised when user not found

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_user_sign_in : UserSignIn
        UserSignIn instance
    """

    auth.users.find_one.return_value = None

    with pytest.raises(SignInWrongCredentials):
        auth.sign_in(user=fake_user_sign_in)


def test_auth_sign_in_password_not_valid(
    auth: Auth,
    fake_find_one_response: FakeFindOneResponse,
    fake_user_sign_in: UserSignIn,
) -> None:
    """
    Test if SignInWrongCredentials exception
    is raised when password not valid

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_find_one_response : FakeFindOneResponse
        Dict with the expected response from find_one method
    fake_user_sign_in : UserSignIn
        UserSignIn instance
    """

    auth.users.find_one.return_value = fake_find_one_response

    with pytest.raises(SignInWrongCredentials):
        auth.sign_in(user=fake_user_sign_in)


def test_auth_sign_in_returns_response(
    auth: Auth,
    fake_find_one_response: FakeFindOneResponse,
    fake_user_sign_in: UserSignIn,
) -> None:
    """
    Test if sign_in method returns the expected response

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_find_one_response : FakeFindOneResponse
        Dict with the expected response from find_one method
    fake_user_sign_in : UserSignIn
        UserSignIn instance
    """

    auth.users.find_one.return_value = fake_find_one_response

    with patch("src.auth.Auth.verify_password") as verify_password_mock:
        verify_password_mock.return_value = True

        response = auth.sign_in(user=fake_user_sign_in)

    assert isinstance(response, AuthResponse)


def test_auth_sign_up_user_already_exists(
    auth: Auth,
    fake_find_one_response: FakeFindOneResponse,
    fake_user_sign_up: UserSignUp,
) -> None:
    """
    Test if UserAlreadyExists exception
    is raised when user already exists

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_find_one_response : FakeFindOneResponse
        Dict with the expected response from find_one method
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    auth.users.find_one.return_value = fake_find_one_response

    with pytest.raises(UserAlreadyExists):
        auth.sign_up(user=fake_user_sign_up)


def test_auth_sign_up_insert_one_called(
    auth: Auth, fake_user_sign_up: UserSignUp
) -> None:
    """
    Test if insert_one method
    is called in sign_up method

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    auth.users.find_one.return_value = None

    auth.sign_up(user=fake_user_sign_up)

    auth.users.insert_one.assert_called_once()


def test_auth_sign_up_returns_response(
    auth: Auth, fake_user_sign_up: UserSignUp
) -> None:
    """
    Test if sign_up method
    returns the expected response

    Parameters
    ----------
    auth : Auth
        Auth instance
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    auth.users.find_one.return_value = None

    response = auth.sign_up(user=fake_user_sign_up)

    assert isinstance(response, AuthResponse)


def test_auth_sign_in_route_200(
    fake_response: AuthResponse, fake_user_sign_in: UserSignIn
) -> None:
    """
    Test the sign_in route with status code 200

    Parameters
    ----------
    fake_response : AuthResponse
        AuthResponse instance
    fake_user_sign_in : UserSignIn
        UserSignIn instance
    """

    with patch("src.auth.router.Auth") as auth_mock:
        auth_mock.return_value.sign_in.return_value = fake_response

        response = client.post(
            "/auth/token",
            data={
                "username": fake_user_sign_in.email,
                "password": fake_user_sign_in.password.get_secret_value(),
            },
        )

    assert response.status_code == 200
    assert response.json() == fake_response.__dict__


def test_auth_sign_up_route_201(
    fake_response: AuthResponse, fake_user_sign_up: UserSignUp
) -> None:
    """
    Test the sign_up route with status code 201

    Parameters
    ----------
    fake_response : AuthResponse
        AuthResponse instance
    fake_user_sign_up : UserSignUp
        UserSignUp instance
    """

    with patch("src.auth.router.Auth") as auth_mock:
        auth_mock.return_value.sign_up.return_value = fake_response

        fake_user_dict = fake_user_sign_up.__dict__
        fake_user_dict["password"] = fake_user_dict["password"].get_secret_value()

        response = client.post("/auth/sign-up", json=fake_user_dict)

    assert response.status_code == 201
    assert response.json() == fake_response.__dict__
