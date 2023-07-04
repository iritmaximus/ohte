from unittest import TestCase, mock
from pytest import mark
import os


from src import config


@mark.config
class TestConfigWithMock(TestCase):
    def test_postgres_db_url_is_set_correctly(self):
        postgres_url = config.db_url()
        # correct port
        self.assertTrue("5432" in postgres_url)

    @mock.patch.dict(os.environ, {"ENV": "test"})
    def test_environment_is_set(self):
        env = config.env()
        self.assertEqual(env, "test")

    @mock.patch.dict(os.environ, {"ENV": "production"}, clear=True)
    def test_postgres_is_not_set(self):
        self.assertRaises(ValueError, config.db_url)

    @mock.patch.dict(os.environ, {"ENV": "test"}, clear=True)
    def test_test_postgres_is_not_set(self):
        self.assertRaises(ValueError, config.db_url)

    @mock.patch.dict(os.environ, clear=True)
    def test_env_not_set(self):
        env = config.env()
        self.assertEqual(env, "production")

    @mock.patch.dict(os.environ, {"POSTGRES_URL": "testurl.com", "ENV": "test"})
    def test_both_are_set(self):
        result = True if config.db_url() and config.env() else False
        self.assertTrue(result)
