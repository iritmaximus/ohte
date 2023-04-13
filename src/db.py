"""
Acts as an interface to a postgresql-db connection
"""
from sqlalchemy import text

import src


def init_db():
    """Creates the sql tables from a schema file"""

    db = create_db_connection(src.engine)
    with open("./src/sql/schema.sql", "r", encoding="utf8") as sqlfile:
        db.execute(text(sqlfile.open()))
    db.close()


def check_user_exists(username: str):
    """Checks if user exists in the database

    :param username: username to check
    :returns: boolean, if user exists
    """
    print(username)


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
    """

    db = create_db_connection()
    sql = """
    SELECT id FROM Users
    WHERE name=:username
    """
    result = db.execute(sql, {"username": username}).fetchall()
    if result:
        raise ValueError("User already exists")

    sql = """
    INSERT INTO Users (name, rating)
    VALUES
        (:username, :rating)
    """
    db.execute(sql, {"username": username, "rating": rating})
    db.close()


def create_db_connection(engine=src.engine):
    """
    Creates a connection based on the engine given.

    :param engine: sqlalchemy engine
    :returns: db connection object
    """
    return engine.connect()
