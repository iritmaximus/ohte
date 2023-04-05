"""
Includes all env variables and other user-modifiable variables

Are implemented as functions because of tests, could just be variables
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv()


def db_url():
    """:returns: the db url defined in .env file"""
    postgres_url = getenv("POSTGRES_URL")
    if not postgres_url:
        raise EnvironmentError("No db url found")
    return postgres_url


def env():
    """:returns: current environment, prod, dev etc"""
    env = getenv("ENV")
    if not env:
        print("ENV not set, defaulting to production")
        env = "production"
    return env
