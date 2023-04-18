"""
API for the chess portion of the app

Implements an interface to interract with the database and
chess rating calculations

TODO:
    Add new game result
    Change game result
    Change if rated game
"""
from fastapi import FastAPI

chess = FastAPI()


@chess.get("/")
async def root():
    return {"message": "This will be the chess api"}
