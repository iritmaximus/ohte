import os
from unittest import TestCase, mock
import config


class TestConfigWithMock(TestCase):
    @mock.patch.dict(os.environ, {"POSTGRES_URL": "testurl.com"})
    def test_postgres_db_url_is_set_correctly(self):
        postgres_url = config.db_url()
        self.assertEqual(postgres_url, "testurl.com")

    @mock.patch.dict(os.environ, {"ENV": "test"})
    def test_environment_is_set(self):
        env = config.env()
        self.assertEqual(env, "test")

    @mock.patch.dict(os.environ, clear=True)
    def test_postgres_is_not_set(self):
        self.assertRaises(EnvironmentError, config.db_url)

    @mock.patch.dict(os.environ, clear=True)
    def test_env_not_set(self):
        env = config.env()
        self.assertEqual(env, "production")

    @mock.patch.dict(os.environ, {"POSTGRES_URL": "testurl.com", "ENV": "test"})
    def test_both_are_set(self):
        result = True if config.db_url() and config.env() else False
        self.assertTrue(result)
