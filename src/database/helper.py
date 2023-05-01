"""
Contains useful helper funtions for dealing with the database
"""
from sqlalchemy import text
from src import engine as default_engine


def check_user_exists(user_id: int, engine=default_engine) -> bool:
    """Checks if user exists by it's id

    It does so by checking if querying for username returns
    anything and returns the corresponding boolean.

    :param user_id: the id of the user
    :param engine: wanted engine to create the db connection with
    :returns: wheter the user exists
    """

    sql = text("SELECT id FROM Users WHERE id=:user_id")
    with engine.connect() as db:
        result = db.execute(sql, {"user_id": user_id}).fetchone()
        if result:
            return True
        return False
