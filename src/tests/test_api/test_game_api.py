from unittest import TestCase, mock
from pytest import mark
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
import os

from src.api import app
from src import config


@mark.userapi
class TestUserApi(TestCase):
    def setUp(self):
        with self.engine.connect() as conn:
            droptablesql = open("./src/sql/droptables.sql", "r")
            schemasql = open("./src/sql/schema.sql", "r")
            conn.execute(text(droptablesql.read()))
            conn.execute(text(schemasql.read()))
            conn.commit()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

        cls.app = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def add_users(self):
        with self.engine.connect() as conn:
            insertusersql = text(
                "INSERT INTO Users (name, rating) VALUES ('moi', 1500), ('hellou', 1215)"
            )
            conn.execute(insertusersql)
            conn.commit()

    def add_games(self):
        with self.engine.connect() as conn:
            sql = text(
                "INSERT INTO Games (result, white_id, black_id) VALUES ('1-0', 1, 2), ('0.5-0.5', 1, 2), ('0-1', 2, 1)"
            )
            conn.execute(sql)
            conn.commit()

    def test_get_all_games_empty(self):
        test_response = {"message": "All played games", "games": []}
        response = self.app.get("/api/games")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_response)

    def test_get_all_games(self):
        self.add_users()
        self.add_games()

        test_games = [[1, "1-0", 1, 2], [2, "0.5-0.5", 1, 2], [3, "0-1", 2, 1]]
        test_response = {"message": "All played games", "games": test_games}
        response = self.app.get("/api/games")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_response)

    def test_add_game(self):
        self.add_users()

        game = {"white_id": "1", "black_id": "2", "result": "1-0"}
        test_return_body = {
            "message": "game created",
            "game": {"white_id": 1, "black_id": 2, "result": "1-0", "rated": True},
        }

        response = self.app.post("/api/games", json=game)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), test_return_body)

    def test_add_game_missing_id(self):
        self.add_users()

        game = {"black_id": "2", "result": "1-0"}
        test_result = {"error": "game creation failed"}

        response = self.app.post("/api/games", json=game)
        self.assertEqual(response.status_code, 422)

    def test_add_game_incorrect_id(self):
        self.add_users()

        game = {"white_id": "2309", "black_id": "2", "result": "1-0"}
        test_result = {
            "error": "game creation failed, 'Both users not found with ids 2309, 2'"
        }

        response = self.app.post("/api/games", json=game)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), test_result)

    def test_add_game_missing_id(self):
        self.add_users()

        game = {"black_id": "2", "result": "1-0"}
        test_result = {
            "error": "game creation failed, 'Both users not found with ids 2309, 2'"
        }

        response = self.app.post("/api/games", json=game)
        self.assertEqual(response.status_code, 422)

    def test_add_game_none_id(self):
        self.add_users()

        game = {"white_id": None, "black_id": "2", "result": "1-0"}
        test_result = {
            "error": "game creation failed, 'Both users not found with ids 2309, 2'"
        }

        response = self.app.post("/api/games", json=game)
        self.assertEqual(response.status_code, 422)

    def test_add_game_incrrect_result(self):
        self.add_users()

        game = {"white_id": "1", "black_id": "2", "result": "1-1"}
        test_result = {
            "error": "game creation failed, Incorrect result value, 1-1, <class 'str'>"
        }

        response = self.app.post("/api/games", json=game)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), test_result)
