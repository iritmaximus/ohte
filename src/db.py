"""
Acts as an interface to a sql-db connection
"""
import psycopg2
import config


def init_db():
    """Creates the sql tables from a schema file"""

    db = psycopg2.connect(config.db_url())
    with open("./src/sql/schema.sql", "r", encoding="utf8") as sqlfile:
        db.execute(sqlfile.open())
    db.close()


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


def create_db_connection():
    """
    Creates db variable to connect to the db depending on the env
    the program is run, test, production and dev

    :returns: db connection object
    """
    if config.env() == "production":
        return psycopg2.connect(config.db_url())
    return psycopg2.connect(config.test_db_url())
