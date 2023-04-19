from unittest import TestCase, mock
from pytest import mark
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
import os

from src.api import app
import src.config as config
import src.db as db


@mark.ratingapi
class TestRating(TestCase):
    def setUp(self):
        conn = db.create_db_connection(self.engine)

        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        conn.execute(text(droptablesql.read()))
        conn.execute(text(schemasql.read()))

        conn.commit()
        conn.close()

    def tearDown(self):
        pass

    def test_get_all_ratings(self):
        self.add_users()
        test_users = {
            "message": "All ratings of users",
            "ratings": [
                {"rating": 1420, "username": "hellou"},
                {"rating": 1300, "username": "moi"},
            ],
        }

        response = self.app.get("/api/rating")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_users)

    def test_get_user_rating_exists(self):
        self.add_users()

        test_response = {
            "message": "Rating of a single user",
            "user": {
                "rating": 1300,
                "username": "moi",
            },
        }
        response = self.app.get("/api/rating/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_response)

    def test_get_user_rating_doest_exist(self):
        test_response = {
            "message": "No user found",
            "user": {},
        }
        response = self.app.get("/api/rating/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), test_response)

    def add_users(self):
        conn = db.create_db_connection(self.engine)
        insertusersql = text(
            "INSERT INTO Users (name, rating) VALUES ('moi', 1300), ('hellou', 1420)"
        )
        conn.execute(insertusersql)

        conn.commit()
        conn.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

        cls.app = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
