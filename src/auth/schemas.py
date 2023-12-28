from pydantic import BaseModel, SecretStr


class User(BaseModel):
    name: str
    email: str
    password: SecretStr


class UserSignIn(BaseModel):
    email: str
    password: SecretStr


class AuthResponse(BaseModel):
    email: str
    access_token: str
    token_type: str = "bearer"
