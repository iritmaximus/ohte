"""
Implements an interface to users

Paths:
    GET     /api/users
    POST    /api/users
    GET     /api/users/<user_id>

    * GET /api/users returns all users
    * POST /api/users creates new user with req body contents
    * GET /api/users/<user_id> returns user with the id

TODO:
    Player id by name           DONE (can be gotten from /api/users/<user_id>)
    Player rating by id         DONE (in /api/rating)

    Add new player              DONE
    Update player rating        DONE
    Update player name
"""

from fastapi import FastAPI, Response
from pydantic import BaseModel

from src.db import get_all_users, create_user, get_user_data, update_user_rating

user_api = FastAPI()


# figure a way to do this without pylint errors
class User(BaseModel):
    """Model for user, for creating new user"""

    username: str
    rating: int | None = None


class Rating(BaseModel):
    """Model for updating rating of an user"""

    rating: int


@user_api.get("/")
async def root():
    """Lists all users in the database

    :returns 200: a list of all users
    """
    users = get_all_users()
    return {"users": users}


@user_api.post("/", status_code=201)
async def api_create_user(item: User, response: Response):
    """Creates a new user to database with users name and rating being
    in req body:
        {"username": str, "rating": int}

    :param item: the req body containing the user data
    :param response: fastapi response obj, can modify status codes

    :returns 201: the new user created
    :returns 404: error with the error message for ex. if the user exists
    """
    try:
        create_user(item.username, item.rating)
    except ValueError as error:
        response.status_code = 403
        return {"error": f"{error}"}
    return {"message": "user created", "user": item}


@user_api.get("/{user_id}")
async def user_by_id(user_id: int | None = None):
    """Get single user by id

    :param user_id: url param for the user id
    :returns 200: the user with the corresponding id
    """
    user = get_user_data(user_id)
    return user


@user_api.put("/{user_id}")
async def update_rating(item: Rating, user_id: int, response: Response):
    """Updates the user rating based on req body

    req body needs to include:
        {"rating": <new_rating>}

    :param user_id: user's id
    :return 201: user gets updated succesfully
    :return 400: incorrect user body
    :return 404: no user found
    """

    try:
        update_user_rating(user_id, item.rating)
        return {"message": "User updated successfully"}
    except ValueError as error:
        response.status_code = 404
        return {"error": f"{error}"}
