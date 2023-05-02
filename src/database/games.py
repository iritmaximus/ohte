"""
Contains all database functions that query Games
"""
from sqlalchemy import text

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
