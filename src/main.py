import re
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.auth.router import auth_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def custom_cors_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Custom CORS middleware to allow
    requests from the frontend

    Parameters
    ----------
    request : Request
        The request object
    call_next : Callable[[Request], Awaitable[Response]]
        The next function to call

    Returns
    -------
    Response
        The response object
    """

    if "origin" in request.headers:
        origin = request.headers["origin"]

        if re.match(r"^https?://task-manager-frontend-.*\.vercel\.app$", origin):
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers[
                "Access-Control-Allow-Methods"
            ] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"

            return response

    return await call_next(request)


app.include_router(auth_router)


@app.get("/")
def root() -> RedirectResponse:
    """
    Redirects to the docs page

    Returns
    -------
    RedirectResponse
        Redirects to the docs page
    """

    return RedirectResponse(url="/docs")
