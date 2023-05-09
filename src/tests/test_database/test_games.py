from unittest import TestCase, mock
from pytest import mark
from sqlalchemy import text, exc, create_engine
import os
import sqlalchemy

import src.database.games as database
from src import config


@mark.database
class TestGames(TestCase):
    def setUp(self):
        self.db = self.engine.connect()

        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        self.db.execute(text(droptablesql.read()))
        self.db.execute(text(schemasql.read()))

        insertusersql = text(
            "INSERT INTO Users (name, rating) VALUES ('moi', 1000), ('hei', 1200)"
        )
        self.db.execute(insertusersql)
        self.db.commit()

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def add_games(self):
        sql = text(
            "INSERT INTO Games (result, white_id, black_id) VALUES ('1-0', 1, 2), ('0.5-0.5', 1, 2), ('0-1', 2, 1)"
        )
        self.db.execute(sql)
        self.db.commit()

    def test_using_test_db(self):
        sql = text("SELECT current_database()")
        db_name = self.db.execute(sql).fetchone()
        self.assertEqual(db_name[0], os.getenv("TEST_POSTGRES_URL").split("/")[-1])

    def test_database_is_empty(self):
        sql = text("SELECT * FROM Games")
        result = self.db.execute(sql).fetchall()
        self.assertEqual(result, [])

    def test_get_all_games(self):
        self.add_games()
        test_result = [
            (1, "1-0", 1, 2),
            (2, "0.5-0.5", 1, 2),
            (3, "0-1", 2, 1),
        ]

        result = database.get_all_games()
        self.assertEqual(result, test_result)

    def test_get_all_games_empty(self):
        result = database.get_all_games()
        self.assertEqual(result, [])

    def test_add_games_helper(self):
        self.add_games()
        test_result = [("1-0",), ("0.5-0.5",), ("0-1",)]

        sql = text("SELECT result FROM Games")
        result = self.db.execute(sql).fetchall()
        self.assertEqual(result, test_result)

    def test_create_game(self):
        database.create_game(1, 2, "1-0", True)
        sql = text("SELECT id FROM GAMES")
        result = self.db.execute(sql).fetchone()
        self.assertEqual(result[0], 1)

    def test_create_game_incorrect_user(self):
        self.assertRaises(KeyError, database.create_game, 1, 10, "1-0", True)

    def test_create_game_incorrect_result(self):
        self.assertRaises(
            ValueError, database.create_game, 1, 2, "0193cd.tbkemjgcrh.pntuea", True
        )

    def test_create_game_incorrect_result_format(self):
        self.assertRaises(ValueError, database.create_game, 1, 2, "1-1", True)

    def test_create_game_incorrect_rated(self):
        self.assertRaises(ValueError, database.create_game, 1, 2, "1-0", "hi")

    def test_create_game_missing_white_id(self):
        self.assertRaises(TypeError, database.create_game, None, 2, "1-0")

    def test_create_game_missing_black_id(self):
        self.assertRaises(TypeError, database.create_game, 1, None, "1-0")

    def test_create_game_missing_black_id(self):
        self.assertRaises(TypeError, database.create_game, 1, 2, None)
