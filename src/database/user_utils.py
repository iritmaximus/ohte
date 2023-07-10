from sqlalchemy import text

from src import engine as default_engine


def parse_user_result_fetchone(result: str) -> list:
    """Parses sqlalchemy query result on table users

    :param result: sqlalchemy query result, the pure result from fetchone()
    :returns: list with all of the fields in the query
    """
    if result:
        result = result[0].strip("()")
        result_list = result.split(",")
        return result_list
    return []


def check_username(username: str, engine=default_engine) -> bool:
    """Checks if user exists in the database

    :param username: username to check
    :param engine: the engine the connection to database is made with

    :returns: boolean, if user exists
    """

    user_id = get_user_id(username, engine)
    if user_id:
        return True
    return False


def get_username(user_id: int, engine=default_engine) -> str:
    """Get user's username by user_id

    :param user_id: id of the user
    :param engine: the engine the connection to database is made with
    :returns: username
    :raises ValueError: if the user or rating doesnt exist
    """

    sql = text("SELECT name FROM Users WHERE id=:user_id")
    with engine.connect() as conn:
        result = conn.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return result[0]
        raise ValueError(f"No user found with id {user_id}")


def get_user_id(username: str, engine=default_engine) -> int | None:
    """Returns the id of the user by it's username

    :param username: username of the user
    :param engine: the engine the connection to database is made with
    :returns: int | None, id of the user or none if no user found
    """

    sql = text("SELECT id FROM Users WHERE name=:username")
    with engine.connect() as conn:
        result = conn.execute(sql, {"username": username}).fetchone()
        if result:
            return result[0]
        return None


def get_user_rating(user_id: int, engine=default_engine) -> int:
    """Queries the database for user's rating

    :param user_id: user_id of the user
    :returns: user's rating rounded to int
    """

    sql = text("SELECT rating FROM Users WHERE id=:user_id")
    with engine.connect() as conn:
        result = conn.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return result[0]
        return -1
