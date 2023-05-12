from unittest import TestCase, mock
from pytest import mark
from sqlalchemy import text, exc, create_engine
import os
import sqlalchemy

from src import config
from src.chess import ChessRating
import src.database.ratings as database


@mark.database
class TestDatabaseRatings(TestCase):
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

    def test_get_user_rating_exists(self):
        result = database.get_user_rating(1)
        self.assertEqual(result, 1000)

    def test_get_user_rating_doesnt_exist(self):
        self.assertRaises(ValueError, database.get_user_rating, 10)

    def test_update_user_rating_exists(self):
        initial_result = database.get_user_rating(1)
        database.update_user_rating(1, 1205)
        changed_result = database.get_user_rating(1)
        self.assertEqual(initial_result, 1000)
        self.assertEqual(changed_result, 1205)

    def test_update_user_rating_doest_exist(self):
        self.assertRaises(ValueError, database.update_user_rating, 10, 1134)

    def test_update_ratings_with_game_result(self):
        test_rating = ChessRating(1000, 1200)
        test_rating.game_result(1, 0)
        test_rating_result = test_rating.white

        database.update_ratings_with_game_result(1, 2, "1-0")
        new_rating = database.get_user_rating(1)
        x = database.get_user_rating(2)
        print(new_rating, x)
        self.assertEqual(new_rating, test_rating_result)

    def tearDown(self):
        self.db.close()

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.db_url())

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
