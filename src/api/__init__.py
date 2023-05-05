from fastapi import FastAPI

from src.api.games import games
from src.api.user import user_api as user
from src.api.rating import rating
from src.api.search import search


app = FastAPI()
app.mount("/api/games", games)
app.mount("/api/users", user)
app.mount("/api/rating", rating)
app.mount("/api/search", search)  # TODO possibly


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
