"""
Contains all database functions having to do with users 
(excluding ratings)
"""
from sqlalchemy import text

from src import engine as default_engine


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

        if result:
            result = result[0].strip("()")
            r_id, r_username = result.split(",")
            return {"id": r_id, "username": r_username}
        return []


def delete_user(user_id: int, engine=default_engine):
    """Deletes user from database based on id

    :param user_id: id of the user that is being deleted
    raises ValueError: if no id
    """
    if not user_id:
        raise ValueError("no id given")

    sql = text("DELETE FROM Users WHERE id=:id")
    with engine.connect() as conn:
        conn.execute(sql, {"id": user_id})
        conn.commit()
