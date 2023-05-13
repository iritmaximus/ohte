"""
Contains all database functions having to do with user's rating
"""
from sqlalchemy import text

from src import engine as default_engine
from src.database.helper import check_user_exists
from src.chess import ChessRating


def get_user_rating(user_id: int, engine=default_engine) -> int:
    """Get user's rating by user_id

    :param user_id: id of the user
    :param engine: the engine the connection to database is made with
    :returns: username
    :raises ValueError: if the user or rating doesnt exist
    """

    sql = text("SELECT rating FROM Users WHERE id=:user_id")
    with engine.connect() as conn:
        result = conn.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return result[0]
        raise ValueError(f"No rating found with id {user_id}")


def get_ratings(engine=default_engine) -> list:
    """Query the database for users sorted by their rating

    :param engine: the engine the connection to database is made with
    :returns: list of users
    """
    sql = text("SELECT rating, name FROM Users ORDER BY rating DESC")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
        # parse empty element out (rating, username,)
        #                                          ^
        return [{"rating": item[0], "username": item[1]} for item in result]


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
