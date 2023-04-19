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
    Player id by name
    Player rating by id         DONE (in /api/rating)

    Add new player              DONE
    Update player rating
    Update player name
"""

from fastapi import FastAPI, Response
from pydantic import BaseModel

from src.db import get_all_users, create_user, get_user_data

user = FastAPI()


# figure a way to do this without pylint errors
class User(BaseModel):
    """Model for user, for creating new user"""

    username: str
    rating: int | None = None


@user.get("/")
async def root():
    """Lists all users in the database

    :returns 200: a list of all users
    """
    users = get_all_users()
    return {"users": users}


@user.post("/", status_code=201)
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
    except ValueError as e:
        response.status_code = 403
        return {"error": f"{e}"}
    return {"message": "user created", "user": item}


@user.get("/{user_id}")
async def user_by_id(user_id: int | None = None):
    """Get single user by id

    :param user_id: url param for the user id
    :returns 200: the user with the corresponding id
    """
    user = get_user_data(user_id)
    return user
