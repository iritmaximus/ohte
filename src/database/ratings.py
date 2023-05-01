"""
Contains all database functions having to do with user's rating
"""
from sqlalchemy import text

from src import engine as default_engine
from src.database.helper import check_user_exists


def get_user_rating(user_id: int, engine=default_engine) -> int:
    """Get user's rating by user_id

    :param user_id: id of the user
    :param engine: the engine the connection to database is made with
    :returns: username
    :raises ValueError: if the user or rating doesnt exist
    """

    sql = text("SELECT rating FROM Users WHERE id=:user_id")
    with engine.connect() as db:
        result = db.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return result[0]
        raise ValueError(f"No rating found with id {user_id}")


def update_user_rating(user_id: int, rating: int, engine=default_engine):
    """
    Updates the rating of a player

    :param user_id: id of the player
    :param rating: new rating of the player ("full rating" not how much it changed)
    :param engine: the engine the connection to database is made with
    :raises ValueError: if the user does not exist
    """
    if not check_user_exists(user_id, engine):
        raise ValueError(f"No user found with id {user_id}")

    sql = text("UPDATE Users SET rating=:rating WHERE id=:user_id")
    with engine.connect() as db:
        db.execute(sql, {"rating": rating, "user_id": user_id})
        db.commit()


def get_ratings(engine=default_engine) -> list:
    """Query the database for users sorted by their rating

    :param engine: the engine the connection to database is made with
    :returns: list of users
    """
    sql = text("SELECT rating, name FROM Users ORDER BY rating DESC")
    with engine.connect() as db:
        result = db.execute(sql).fetchall()
        # parse empty element out (rating, username,)
        #                                          ^
        return [{"rating": item[0], "username": item[1]} for item in result]
