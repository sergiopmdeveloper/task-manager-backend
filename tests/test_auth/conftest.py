from unittest.mock import patch

import pytest
from bson import ObjectId
from pytest import MonkeyPatch

from src.auth.Auth import Auth
from src.auth.schemas import AuthResponse, UserSignIn, UserSignUp, VerifyTokenResponse
from tests.test_auth.types import FakeFindOneResponse


@pytest.fixture
def fake_user_sign_up() -> UserSignUp:
    """
    Returns a UserSignUp instance

    Returns
    -------
    UserSignUp
        UserSignUp instance
    """

    return UserSignUp(name="fake_name", email="fake_email", password="fake_password")


@pytest.fixture
def fake_user_sign_in() -> UserSignIn:
    """
    Returns a UserSignIn instance

    Returns
    -------
    UserSignIn
        UserSignIn instance
    """

    return UserSignIn(email="fake_email", password="fake_password")


@pytest.fixture
def fake_find_one_response() -> FakeFindOneResponse:
    """
    Returns a dict with the expected
    response from find_one method

    Returns
    -------
    FakeFindOneResponse
        Dict with the expected response
    """

    return {
        "_id": ObjectId("60d5ec9af682fbd39d1b1681"),
        "name": "fake_name",
        "email": "fake_email",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }


@pytest.fixture
def fake_response() -> AuthResponse:
    """
    Returns an AuthResponse instance

    Returns
    -------
    AuthResponse
        AuthResponse instance
    """

    return AuthResponse(
        name="fake_name", email="fake_email", access_token="fake_access_token"
    )


@pytest.fixture
def fake_verify_token_response() -> VerifyTokenResponse:
    """
    Returns a VerifyTokenResponse instance

    Returns
    -------
    VerifyTokenResponse
        VerifyTokenResponse instance
    """

    return VerifyTokenResponse(detail="Token is valid")


@pytest.fixture
def auth(monkeypatch: MonkeyPatch) -> Auth:
    """
    Returns an Auth instance

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items

    Returns
    -------
    Auth
        Auth instance
    """

    monkeypatch.setenv("JWT_SECRET_KEY", "fake_jwt_secret_key")

    with patch("src.auth.Auth.Database.get_client"):
        auth = Auth()

    return auth
