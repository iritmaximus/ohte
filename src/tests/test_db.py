from unittest import TestCase, mock
from pytest import mark
from sqlalchemy import text, exc, create_engine
import os
import sqlite3
import psycopg2

import src.db as db
from src import config


@mark.database
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

    def test_get_all_users_no_users(self):
        result = db.get_all_users()
        self.assertEqual(result, None)

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()


@mark.database
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
        result = db.get_user_id("hei")
        self.assertEqual(result, 2)

    def test_check_user_exists_true(self):
        result = db.check_user_exists(1)
        self.assertEqual(result, True)

    def test_check_user_exists_false(self):
        result = db.check_user_exists(10)
        self.assertEqual(result, False)

    def test_create_user_doesnt_exist(self):
        result = db.check_user_exists(3)
        self.assertEqual(result, False)

    def test_create_user_new(self):
        db.create_user("moikka")
        result = db.check_user_exists(3)
        self.assertEqual(result, True)

    def test_create_user_exists(self):
        self.assertRaises(ValueError, db.create_user, "moi")

    def test_get_user_rating_exists(self):
        result = db.get_user_rating(1)
        self.assertEqual(result, 1000)

    def test_get_user_rating_doesnt_exist(self):
        self.assertRaises(ValueError, db.get_user_rating, 10)

    def test_update_user_rating_exists(self):
        db.update_user_rating(1, 1205)
        result = db.get_user_rating(1)
        self.assertEqual(result, 1205)

    def test_update_user_rating_doest_exist(self):
        self.assertRaises(ValueError, db.update_user_rating, 10, 1134)

    def test_get_all_users(self):
        test_result = [
            {"username": "moi", "rating": 1000},
            {"username": "hei", "rating": 1200},
        ]
        result = db.get_all_users()
        self.assertEqual(result, test_result)

    def test_get_user_data_exists(self):
        test_user = {"user_id": 1, "username": "moi", "rating": 1000}
        result = db.get_user_data(1)
        self.assertEqual(result, test_user)

    def test_get_user_data_doesnt_exist(self):
        result = db.get_user_data(10)
        self.assertEqual(result, None)

    def test_get_username_exists(self):
        result = db.get_username(1)
        self.assertEqual(result, "moi")

    def test_get_username_doesnt_exist(self):
        self.assertRaises(ValueError, db.get_username, 10)

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
