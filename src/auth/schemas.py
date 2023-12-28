from pydantic import BaseModel, SecretStr


class User(BaseModel):
    name: str
    email: str
    password: SecretStr


class UserSignIn(BaseModel):
    email: str
    password: SecretStr


class SignUpResponse(BaseModel):
    user_id: str
    access_token: str


class SignInResponse(BaseModel):
    email: str
    access_token: str
    token_type: str = "bearer"
