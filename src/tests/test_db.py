from unittest import TestCase, mock
import os
from src import config
import src.db as db
import sqlite3
import psycopg2


@mock.patch.dict(os.environ, {"POSTGRES_URL": os.getenv("TEST_POSTGRES_URL")})
class TestDBPostgresWithoutItems(TestCase):
    def setUp(self):
        self.db = db.create_db_connection()
        self.cur = self.db.cursor()
        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        self.cur.execute(droptablesql.read())
        self.cur.execute(schemasql.read())
        self.db.commit()

    def test_using_test_db(self):
        env = config.env()
        self.assertEqual(env, "test")

    def test_creating_db_conn_obj(self):
        database = db.create_db_connection()
        self.assertIsInstance(database, psycopg2.extensions.connection)

    def test_tables_created_and_empty_games(self):
        sql = "SELECT * FROM Games"
        self.cur.execute(sql)
        result = self.cur.fetchone()
        self.assertEqual(result, None)

    def test_tables_created_and_empty_users(self):
        sql = "SELECT * FROM Users"
        self.cur.execute(sql)
        result = self.cur.fetchone()
        self.assertEqual(result, None)

    def test_error_if_table_not_created(self):
        sql = "DROP TABLE IF EXISTS Users CASCADE"
        self.cur.execute(sql)
        self.db.commit()
        selectsql = "SELECT * FROM Users"
        self.assertRaises(psycopg2.errors.UndefinedTable, self.cur.execute, selectsql)

    def test_insert_one_user(self):
        sql = "INSERT INTO Users (name, rating) VALUES ('moi', 1000)"
        self.cur.execute(sql)
        self.db.commit()

        self.cur.execute("SELECT name FROM Users")
        result = self.cur.fetchone()
        self.assertEqual(result[0], "moi")

    def tearDown(self):
        self.cur.close()
        self.db.close()


@mock.patch.dict(os.environ, {"POSTGRES_URL": os.getenv("TEST_POSTGRES_URL")})
class TestPostgresItems(TestCase):
    def setUp(self):
        self.db = db.create_db_connection()
        self.cur = self.db.cursor()
        droptablesql = open("./src/sql/droptables.sql", "r")
        schemasql = open("./src/sql/schema.sql", "r")
        self.cur.execute(droptablesql.read())
        self.cur.execute(schemasql.read())

        insertusersql = (
            "INSERT INTO Users (name, rating) VALUES ('moi', 1000), ('hei', 1200)"
        )
        self.cur.execute(insertusersql)
        self.db.commit()

    def test_test_users_in_db(self):
        sql = "SELECT name FROM Users"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.assertEqual(result, [("moi",), ("hei",)])
