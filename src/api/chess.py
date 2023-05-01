"""
API for the chess portion of the app

Implements an interface to interract with the database and
chess rating calculations

TODO:
    Add new game result
    Change game result
    Change if rated game
    Update players's ratings
"""
from fastapi import FastAPI

chess = FastAPI()


@chess.get("/games")
async def list_all_games():
    """Returns a list of all games that have been played

    :returns: list of all games played
    """
    return {"message": "A list of all games played", "games": []}


@chess.get("/")
async def root():
    return {"message": "This will be the chess api"}
