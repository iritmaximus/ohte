from fastapi import FastAPI

from src.api.chess import chess
from src.api.user import user
from src.api.rating import rating
from src.api.search import search


app = FastAPI()
app.mount("/api/chess", chess)
app.mount("/api/users", user)
app.mount("/api/rating", rating)
app.mount("/api/search", search)  # TODO possibly


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
