"""
Acts as an interface to a postgresql-db connection
"""

from sqlalchemy import text
from typing import Tuple  # for type hint

import src


def check_user_exists(username: str):
    """Checks if user exists in the database

    :param username: username to check
    :returns: boolean, if user exists
    """

    user_id = get_user_id(username)
    if user_id:
        return True
    return False


def get_all_users():
    """Queries the database for all users and their ratings

    :returns: list of users and ratings
    """

    sql = text("SELECT name, rating FROM Users")
    with create_db_connection() as db:
        result = db.execute(sql).fetchall()
        if result:
            rows = []
            for x in result:
                rows.append({"username": x[0], "rating": x[1]})
            return rows
        return None


def get_user_rating(user_id: int):
    """Get user's rating by user_id

    :param user_id: id of the user
    :raises ValueError: if the user or rating doesnt exist
    """

    if get_user_data(user_id) is None:
        raise ValueError(f"No user found with id {user_id}")

    sql = text("SELECT rating FROM Users WHERE id=:user_id")
    with create_db_connection() as db:
        result = db.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return result[0]
        raise ValueError(f"No rating found with id {user_id}")


def get_user_id(username: str) -> int | None:
    """Returns the id of the user by it's username

    :param username: username of the user
    :returns: int | None, id of the user or none if no user found
    """

    sql = text("SELECT id FROM Users WHERE name=:username")
    with create_db_connection() as db:
        result = db.execute(sql, {"username": username}).fetchone()
        if result:
            return result[0]
        return None


def get_user_data(user_id: int):
    """Queries the database for user by id and returns
        user id,
        name,
        rating

    :param user_id: id of the user
    :returns: user id, name and rating as dict | None if no user found
    """

    sql = text("SELECT id, name, rating FROM Users WHERE id=:user_id")
    with create_db_connection() as db:
        result = db.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return {"user_id": result[0], "username": result[1], "rating": result[2]}
        return None


def create_user(username: str, rating: int = 1200):
    """
    Creates a new user with username and rating and inserts it to the db

    :param username: username of the new user
    :param rating: the rating the new user has (defaults to 1200)
    :raises ValueError: if user exists with username
    """

    if check_user_exists(username):
        raise ValueError("User already exists")

    with create_db_connection() as db:
        sql = text("INSERT INTO Users (name, rating) VALUES (:username, :rating)")
        db.execute(sql, {"username": username, "rating": rating})
        db.commit()


def update_user_rating(user_id: int, rating: int):
    """
    Updates the rating of a player

    :param user_id: id of the player
    :param rating: new rating of the player ("full rating" not how much it changed)
    :raises ValueError: if the user does not exist
    """

    if get_user_data(user_id) is None:
        raise ValueError(f"No user found with id {user_id}")

    sql = text("UPDATE Users SET rating=:rating WHERE id=:user_id")
    with create_db_connection() as db:
        db.execute(sql, {"rating": rating, "user_id": user_id})
        db.commit()


def create_db_connection(engine=src.engine):
    """
    Creates a connection based on the engine given.

    :param engine: sqlalchemy engine
    :returns: db connection object
    """
    return engine.connect()
