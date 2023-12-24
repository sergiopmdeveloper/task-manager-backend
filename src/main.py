from fastapi import FastAPI
from fastapi.responses import RedirectResponse

"""
API entry point
"""

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs/")
