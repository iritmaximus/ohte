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

    def test_using_test_db(self):
        sql = text("SELECT current_database()")
        db_name = self.db.execute(sql).fetchone()
        self.assertEqual(db_name[0], os.getenv("TEST_POSTGRES_URL").split("/")[-1])

    def test_database_is_empty(self):
        sql = text("SELECT * FROM Games")
        result = self.db.execute(sql).fetchall()
        self.assertEqual(result, [])

    def test_create_games(self):
        self.add_games()
        test_result = [("1-0",), ("0.5-0.5",), ("0-1",)]

        sql = text("SELECT result FROM Games")
        result = self.db.execute(sql).fetchall()
        self.assertEqual(result, test_result)

    # id serial primary key not null,
    # result varchar(10),
    # white_id integer,
    # black_id integer,
    # rated boolean default true,
    # def test_get_all_games(self):
    #     self.add_games()
    #     test_result = [
    #         {1},
    #         {2},
    #         {3},
    #     ]

    #     result = database.get_all_games()
    #     self.assertEqual(result, test_result)

    def add_games(self):
        sql = text(
            "INSERT INTO Games (result, white_id, black_id) VALUES ('1-0', 1, 2), ('0.5-0.5', 1, 2), ('0-1', 2, 1)"
        )
        self.db.execute(sql)
        self.db.commit()

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
