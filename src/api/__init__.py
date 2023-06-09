"""Connects all url paths together, implements app variable"""

from fastapi import FastAPI

from src.api.games import games
from src.api.user import user_api as user


app = FastAPI()
app.mount("/api/games", games)
app.mount("/api/users", user)


@app.get("/")
async def root():
    """Test page to greet the user when querying the base url :)"""
    return {"message": "Hello, world!"}
