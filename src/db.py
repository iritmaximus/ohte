"""
Acts as an interface to a sql-db connection
"""
import sqlite3


def test_db():
    """Creates a test db and initializes it"""
    # FIXME move to proper test db
    # TODO Execute the schema from a file

    db = sqlite3.connect("test.db")
    sql = """
    CREATE TABLE IF NOT EXISTS Users (
            id integer primary key autoincrement not null,
            name varchar(255) not null,
            rating integer
    )
    """
    db.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS Games (
            id integer primary key autoincrement not null,
            result varchar(10),
            user_id integer not null,
            foreign key (user_id)
                references Users (id)
    )
    """
    db.execute(sql)
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
    Creates db variable to connect to the db

    :returns: db connection object
    """
    # FIXME move this to be a proper database when get home
    return sqlite3.connect("test.db")


if __name__ == "__main__":
    test_db()
