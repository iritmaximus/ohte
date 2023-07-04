"""
Works as an interface to users's ratings

Paths:
    GET     /api/rating
    GET     /api/rating/<user_id>

    * /api/rating returns all users sorted by their rating, in
    descending order
    * /api/rating/<user_id> returns users rating, and also their username.

TODO:
    How much rating has changed
        Fancy graphs?
        Modifiable time window?
    Dedicated leaderboard
"""

from fastapi import FastAPI, Response

from src.database.ratings import get_ratings
from src.database.user import get_one_user

rating = FastAPI()


@rating.get("/")
async def all_user_ratings():
    """Queries the database for all users and sorts them by rating

    :returns 200: the list of users sorted by rating
    """
    ratings = get_ratings()
    return {"message": "All ratings of users", "ratings": ratings}


@rating.get("/{user_id}", status_code=200)
async def user_rating(user_id: int | None, response: Response):
    """Queries the database for only the rating of one player

    :returns 200: the user' rating
    :returns 404: if user with the id is not found
    """
    # TODO queries unneccesary information + needs to format data
    user = get_one_user(user_id)
    if user:
        user_sorted = {"rating": user["rating"], "username": user["username"]}
        return {"message": "Rating of a single user", "user": user_sorted}
    response.status_code = 404
    return {"message": "No user found", "user": {}}
