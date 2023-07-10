"""
Contains all database functions having to do with users 
(excluding ratings)
"""
from sqlalchemy import text

from src import engine as default_engine
from src.database.helper import check_user_exists
from src.database.user_utils import (
    check_username,
    get_user_rating,
    parse_user_result_fetchone,
)
from src.chess import ChessRating


def get_one_user(user_id: int, engine=default_engine) -> dict:
    """Queries the database for user by id and returns
        user id,
        name,
        rating

    :param user_id: id of the user
    :param engine: wanted engine to create the db connection with
    :returns: user id, name and rating as dict | None if no user found
    """

    sql = text("SELECT id, name, rating FROM Users WHERE id=:id")
    with engine.connect() as conn:
        result = conn.execute(sql, {"id": user_id}).fetchone()
        if result:
            return {"id": result[0], "username": result[1], "rating": result[2]}
        return None


def get_all_users(engine=default_engine) -> list:
    """Queries the database for all users and their ratings

    :param engine: wanted engine to create the db connection with
    :returns: list of users and ratings
    """

    sql = text("SELECT id, name, rating FROM Users")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
        if result:
            rows = []
            for item in result:
                rows.append({"id": item[0], "username": item[1], "rating": item[2]})
            return rows
        return None


def create_user(username: str, password_hash: str, engine=default_engine) -> list:
    """
    Creates a new user with username and rating and inserts it to the db

    :param username: username of the new user
    :param password_hash: users password hashed NOT IN CLEARTEXT
    :param engine: wanted engine to create the db connection with
    :raises ValueError: if user exists with username
    """

    if not username:
        raise ValueError("No username given")
    if not password_hash:
        raise ValueError("Password not defined")
    if check_username(username, engine):
        raise ValueError("User already exists")

    with engine.connect() as conn:
        sql = text(
            """
        INSERT INTO Users 
            (name, password_hash) 
        VALUES 
            (:username, :password_hash)
        RETURNING
            (Users.id, Users.name) 
        """
        )
        result = conn.execute(
            sql, {"username": username, "password_hash": password_hash}
        ).fetchone()
        conn.commit()
        return parse_user_result_fetchone(result)


def delete_user(user_id: int, engine=default_engine):
    """Deletes user from database based on id

    :param user_id: id of the user that is being deleted
    raises ValueError: if no id
    """
    if not user_id:
        raise ValueError("no id given")

    sql = text(
        "DELETE FROM Users WHERE id=:id RETURNS Users.id, Users.name, Users.rating"
    )
    with engine.connect() as conn:
        result = conn.execute(sql, {"id": user_id}).fetchone()
        conn.commit()
        return parse_user_result_fetchone(result)


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
    with engine.connect() as conn:
        conn.execute(sql, {"rating": rating, "user_id": user_id})
        conn.commit()


def update_ratings_with_game_result(
    white_id: int, black_id: int, result: str, engine=default_engine
):
    """Updates players ratings to database according to a game result

    :param white_id: id of the white player
    :param black_id: id of the black player
    :param result: game result, either 1-0, 0-1 or 0.5-0.5 as a string
    :param engine: engine to make connections with
    :raises ValueError: if initial ratings cant be found for both users
    """

    white_rating = get_user_rating(white_id)
    black_rating = get_user_rating(black_id)
    if not white_rating or not black_rating:
        raise ValueError("Ratings for both users not found")

    ratings = ChessRating(white_rating, black_rating)
    result_list = result.split("-")
    ratings.game_result(float(result_list[0]), float(result_list[1]))

    sql = text(
        """
    UPDATE Users SET 
        rating = New.rating
    FROM (VALUES
        (:white_id, :white_rating),
        (:black_id, :black_rating)
    ) AS New (id, rating)
    WHERE Users.id=New.id
    """
    )

    # TODO tests for incorrect values and such
    with engine.connect() as conn:
        conn.execute(
            sql,
            {
                "white_id": white_id,
                "white_rating": ratings.white,
                "black_id": black_id,
                "black_rating": ratings.black,
            },
        )
        conn.commit()
