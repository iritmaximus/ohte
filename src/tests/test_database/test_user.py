from unittest import TestCase, mock
from pytest import mark
from sqlalchemy import text, exc, create_engine
import os
import sqlite3
import psycopg2

import src.database.helper as helper
import src.database.user as database
from src import config


@mark.database
class TestDatabaseUser(TestCase):
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

    def test_test_users_in_db(self):
        sql = text("SELECT name FROM Users")
        result = self.db.execute(sql).fetchall()
        self.assertEqual(result, [("moi",), ("hei",)])

    def test_get_user_id(self):
        result = database.get_user_id("hei")
        self.assertEqual(result, 2)

    def test_create_user_doesnt_exist(self):
        result = helper.check_user_exists(3)
        self.assertEqual(result, False)

    def test_create_user_new(self):
        database.create_user("moikka", 1200)
        result = helper.check_user_exists(3)
        self.assertEqual(result, True)

    def test_create_user_exists(self):
        self.assertRaises(ValueError, database.create_user, "moi")

    def test_get_all_users(self):
        test_result = [
            {"username": "moi", "rating": 1000},
            {"username": "hei", "rating": 1200},
        ]
        result = database.get_all_users(self.engine)
        self.assertEqual(result, test_result)

    def test_get_user_data_exists(self):
        test_user = {"user_id": 1, "username": "moi", "rating": 1000}
        result = database.get_user_data(1)
        self.assertEqual(result, test_user)

    def test_get_user_data_doesnt_exist(self):
        result = database.get_user_data(10)
        self.assertEqual(result, None)

    def test_get_username_exists(self):
        result = database.get_username(1)
        self.assertEqual(result, "moi")

    def test_get_username_doesnt_exist(self):
        self.assertRaises(ValueError, database.get_username, 10)

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
