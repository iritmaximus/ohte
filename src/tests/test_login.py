from unittest import TestCase
import bcrypt

import src.utils.login as login

class TestLogin(TestCase):
    def test_creates_password_hash_returns_str(self):
        password_hash = login.create_password_hash("unsecure")
        self.assertIsInstance(password_hash, str)

    def test_create_password_fails_if_no_password(self):
        self.assertRaises(TypeError, login.create_password_hash)

    def test_create_password_doesnt_fail_on_incorrect_input_type(self):
        password_hash = login.create_password_hash(23985702)
        self.assertIsInstance(password_hash, str)


    def test_check_password_success_on_correct_password(self):
        password_hash = login.create_password_hash("unsecure")
        self.assertEqual(login.check_password("unsecure", password_hash), True)

    def test_check_password_fail_on_incorrect_password(self):
        true_password = "totallysecurepassword"
        incorrect_password = "hellurei"
        password_hash = login.create_password_hash(true_password)
        self.assertFalse(login.check_password(incorrect_password, password_hash))

    def test_check_password_fail_on_no_password(self):
        password_hash = login.create_password_hash("unsecure")
        self.assertFalse(login.check_password(None, password_hash))

    def test_check_password_fail_on_incorrect_type(self):
        password_hash = login.create_password_hash("unsecure")
        self.assertFalse(login.check_password(52340987, password_hash))
