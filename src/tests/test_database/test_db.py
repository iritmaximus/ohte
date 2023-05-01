from unittest import TestCase, mock
from pytest import mark
from sqlalchemy import text, exc, create_engine
import os
import sqlalchemy
import src.database.helper as helper
import src.database.user as database
from src import config


@mark.database
class TestDatabaseBase(TestCase):
    def setUp(self):
        self.db = self.engine.connect()
        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        self.db.execute(text(droptablesql.read()))
        self.db.execute(text(schemasql.read()))
        self.db.commit()

    def test_using_test_db(self):
        sql = text("SELECT current_database()")
        db_name = self.db.execute(sql).fetchone()
        self.assertEqual(db_name[0], os.getenv("TEST_POSTGRES_URL").split("/")[-1])

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
        self.add_user()

        sql = text("SELECT name FROM Users")
        result = self.db.execute(sql).fetchone()
        self.assertEqual(result[0], "moi")

    def test_get_all_users_no_users(self):
        result = database.get_all_users()
        self.assertEqual(result, None)

    def test_check_user_exists_true(self):
        self.add_user()

        result = helper.check_user_exists(1)
        self.assertEqual(result, True)

    def test_check_user_exists_false(self):
        result = helper.check_user_exists(10)
        self.assertEqual(result, False)

    def add_user(self):
        sql = text("INSERT INTO Users (name, rating) VALUES ('moi', 1000)")
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
