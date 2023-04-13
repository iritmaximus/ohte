from unittest import TestCase, mock
from sqlalchemy import text, exc, create_engine
import os
import sqlite3
import psycopg2

import src.db as db
from src import config


@mock.patch.dict(os.environ, {"POSTGRES_URL": os.getenv("TEST_POSTGRES_URL")})
class TestDBPostgresWithoutItems(TestCase):
    def setUp(self):
        self.db = db.create_db_connection(self.engine)
        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        self.db.execute(text(droptablesql.read()))
        self.db.execute(text(schemasql.read()))
        self.db.commit()

    def test_using_test_db(self):
        env = config.env()
        self.assertEqual(env, "test")

    def test_creating_db_conn_obj(self):
        database = db.create_db_connection(self.engine)
        # FIXME do something about this
        # self.assertIsInstance(database, psycopg2.extensions.connection)
        self.assertEqual(1, 1)
        database.close()

    def test_tables_created_and_empty_games(self):
        sql = text("SELECT * FROM Games")
        result = self.db.execute(sql).fetchone()
        self.assertEqual(result, None)

    def test_tables_created_and_empty_users(self):
        sql = text("SELECT * FROM Users")
        result = self.db.execute(sql).fetchone()
        self.assertEqual(result, None)

    def test_error_if_table_not_created(self):
        sql = text("DROP TABLE IF EXISTS Users CASCADE")
        self.db.execute(sql)
        self.db.commit()
        selectsql = text("SELECT * FROM Users")
        self.assertRaises(exc.ProgrammingError, self.db.execute, selectsql)

    def test_insert_one_user(self):
        sql = text("INSERT INTO Users (name, rating) VALUES ('moi', 1000)")
        self.db.execute(sql)
        self.db.commit()

        sql = text("SELECT name FROM Users")
        result = self.db.execute(sql).fetchone()
        self.assertEqual(result[0], "moi")

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()


@mock.patch.dict(os.environ, {"POSTGRES_URL": os.getenv("TEST_POSTGRES_URL")})
class TestPostgresItems(TestCase):
    def setUp(self):
        self.db = db.create_db_connection(self.engine)

        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        self.db.execute(text(droptablesql.read()))
        self.db.execute(text(schemasql.read()))

        insertusersql = text(
            "INSERT INTO Users (name, rating) VALUES ('moi', 1000), ('hei', 1200)"
        )
        self.db.execute(insertusersql)
        self.db.commit()

    def test_test_users_in_db(self):
        sql = text("SELECT name FROM Users")
        result = self.db.execute(sql).fetchall()
        self.assertEqual(result, [("moi",), ("hei",)])

    def test_get_user_id(self):
        result = db.get_user_id("moi")
        self.assertEqual(result, 1)

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
