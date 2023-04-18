"""
Implements an interface to users

TODO:
    Player id by name
    Player rating by id

    Add new player
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

    name: str
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
        {"name": str, "rating": int}

    :param item: the req body containing the user data
    :param response: fastapi response obj, can modify status codes

    :returns 201: the new user created
    :returns 404: error with the error message for ex. if the user exists
    """
    try:
        create_user(item.name, item.rating)
    except ValueError as e:
        response.status_code = 404
        return {"error": f"{e}"}
    return {"message": "ok", "user": item}


@user.get("/{user_id}")
async def user_by_id(user_id: int | None = None):
    """Get single user by id

    :param user_id: url param for the user id
    :returns 200: the user with the corresponding id
    """
    user = get_user_data(user_id)
    return {"user_id": user[0], "username": user[1], "rating": user[2]}
