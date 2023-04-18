from unittest import TestCase, mock
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
import os

from src.api import app
import src.config as config
import src.db as db


@mock.patch.dict(os.environ, {"POSTGRES_URL": os.getenv("TEST_POSTGRES_URL")})
class TestUserApi(TestCase):
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

    def test_get_all_users(self):
        self.add_users()

        test_users = {
            "users": [
                {"username": "moi", "rating": 1500},
                {"username": "hellou", "rating": 1215},
            ]
        }
        response = self.app.get("/api/users").json()
        self.assertEqual(response, test_users)

    def test_get_user_by_id(self):
        self.add_users()

        test_user = {"user_id": 1, "username": "moi", "rating": 1500}
        response = self.app.get("/api/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_user)

    def test_create_user_correct_doesnt_exist(self):
        user = {"username": "moikku", "rating": 1300}
        test_return_body = {
            "message": "user created",
            "user": {"username": "moikku", "rating": 1300},
        }
        response = self.app.post("/api/users", json=user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), test_return_body)

    def test_create_user_correct_exists(self):
        self.add_users()

        user = {"username": "moi", "rating": 1300}
        response = self.app.post("/api/users", json=user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"error": "User already exists"})

    def test_create_user_incorrect(self):
        user = {"name": "moi", "rating": 1300}
        response = self.app.post("/api/users", json=user)
        self.assertEqual(response.status_code, 422)

    def add_users(self):
        conn = db.create_db_connection(self.engine)
        insertusersql = text(
            "INSERT INTO Users (name, rating) VALUES ('moi', 1500), ('hellou', 1215)"
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
