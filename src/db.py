"""
Acts as an interface to a postgresql-db connection
"""
from sqlalchemy import text

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


def get_user_rating(username: str):
    """Get user's rating by username

    :param username: username of the user
    :raises ValueError: if the user doesnt exist
    """
    user_id = get_user_id(username)
    if not user_id:
        raise ValueError("User not found")

    sql = text("SELECT rating FROM Users WHERE id=:user_id")
    with create_db_connection() as db:
        result = db.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return result[0]

        # cant test this :( rip 100% as to result to be none would mean something went wrong with
        # the connection (internet) or there was concurrency errors
        raise ValueError(f"No rating found for id {user_id}")


def get_user_id(username: str):
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


def update_user_rating(username: str, rating: int):
    """
    Updates the rating of a player
    :param username: username of the player
    :param rating: new rating of the player ("full rating" not how much it changed)
    :raises ValueError: if the user does not exist
    """
    if not check_user_exists(username):
        raise ValueError("User does not exist")
    user_id = get_user_id(username)

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
