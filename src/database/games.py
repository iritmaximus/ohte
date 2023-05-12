"""
Contains all database functions that query Games
"""
from sqlalchemy import text, exc

from src import engine as default_engine


def get_all_games(engine=default_engine):
    """Returns all games played

    :param engine: engine to make connection with the database
    :returns: list of all games or empty list
    """

    sql = text("SELECT * FROM Games")
    with engine.connect() as db:
        result = db.execute(sql).fetchall()
        if result:
            return [(x[:-1]) for x in result]
        return []


def create_game(
    white_id: int, black_id: int, result: str, rated: bool = True, engine=default_engine
):
    """Creates new user to database

    :param white_id: white player's id
    :param black_id: black's id
    :param result: the result of the game, 1-0, 0-1 or 0.5-0.5
    :param rated: if the game is rated and counted to the rating
    :param engine: the engine to connect to the database with

    :raises ValueError:, if values are incorrect format
    :raises TypeError:, if values are not set
    :raises KeyError: if users don't exist
    """
    sql = text(
        """
    INSERT INTO Games
        (white_id, black_id, result, rated)
    VALUES
        (:white_id, :black_id, :result, :rated)
    """
    )
    if white_id is None or black_id is None or result is None:
        raise TypeError("All values not set")

    if result not in ["1-0", "0-1", "0.5-0.5"]:
        raise ValueError(f"Incorrect result value, {result}, {type(result)}")

    try:
        with engine.connect() as conn:
            conn.execute(
                sql,
                {
                    "white_id": white_id,
                    "black_id": black_id,
                    "result": result,
                    "rated": rated,
                },
            )
            conn.commit()

    except exc.IntegrityError as error:
        raise KeyError(
            f"Both users not found with ids {white_id}, {black_id}"
        ) from error
    except exc.DataError as error:
        raise ValueError(f"Incorrect values given, {error}") from error
