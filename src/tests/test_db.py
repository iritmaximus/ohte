import unittest
import src.db
import sqlite3


class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect("test.db")

        # TODO move to executing the schema from file
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
                id integer primary key autoincrement not null,
                name varchar(255) not null,
                rating integer
        )
        """
        self.db.execute(sql)
        sql = """
        CREATE TABLE IF NOT EXISTS Games (
                id integer primary key autoincrement not null,
                result varchar(10),
                user_id integer not null,
                foreign key (user_id)
                    references Users (id)
        )
        """
        self.db.execute(sql)

    def tearDown(self):
        self.db.close()

    def test_creating_user(self):
        username = "moi"
        rating = 1200
        sql = """
        INSERT INTO Users (name, rating)
        VALUES (:username, :rating)
        """
        self.db.execute(sql, {"username": username, "rating": rating})
        result = self.db.execute("SELECT name FROM Users").fetchone()
        self.assertEqual(result[0], "moi")
