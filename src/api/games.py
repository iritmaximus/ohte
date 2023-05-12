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
from fastapi import FastAPI, Response
from pydantic import BaseModel

from src.database.games import get_all_games, create_game
from src.database.ratings import update_ratings_with_game_result


games = FastAPI()


class GameResult(BaseModel):
    """Request body structure of create_game"""

    white_id: int
    black_id: int
    result: str
    rated: bool = True


@games.get("/", status_code=200)
async def list_all_games():
    """Returns a list of all games that have been played

    :returns 200: list of all games played
    """
    all_games = get_all_games()
    return {"message": "All played games", "games": all_games}


@games.post("/", status_code=201)
async def create_new_game(item: GameResult, response: Response):
    """Creates a new game based on the request body

    Request body should contain:
        white_id: id of the player playing white
        black_id: id of the player playing black
        result: the result of the game represented by 1-0, 0-1 or 0.5-0.5
        rated: if the game should be counted to the rating of the players

    :returns 201: game created successfully
    :returns 400: error adding the user to database
    :returns 404: user not found or other error
    """
    try:
        create_game(item.white_id, item.black_id, item.result, item.rated)
    except ValueError as error:
        response.status_code = 400
        return {"error": f"game creation failed, {error}"}
    except KeyError as error:
        response.status_code = 404
        return {"error": f"game creation failed, {error}"}

    # calculate new ratings for the players
    try:
        update_ratings_with_game_result(item.white_id, item.black_id, item.result)
    except ValueError as error:
        return {"error": f"rating calculation failed, {error}"}

    return {
        "message": "game created",
        "game": {
            "white_id": item.white_id,
            "black_id": item.black_id,
            "result": item.result,
            "rated": item.rated,
        },
    }
