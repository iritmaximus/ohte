"""
Includes all env variables and other user-modifiable variables

Are implemented as functions because of tests, could just be variables
"""

from os import getenv


def db_url() -> str:
    """Returns the postgres db url depending on the environment variable ENV
    ENV==production returns POSTGRES_URL
    ENV==test returns TEST_POSTGRES_URL

    :returns: the url
    :raises ValueError: if the url is not found
    """

    env_var = env()
    if env_var == "production":
        url_var = getenv("POSTGRES_URL", None)
        if url_var is None:
            raise ValueError(
                f"Environment variable POSTGRES_URL not set, found {url_var}"
            )
        return url_var

    test_url_var = getenv("TEST_POSTGRES_URL", None)
    if test_url_var is None:
        raise ValueError(
            f"Environment variable TEST_POSTGRES_URL not set, found {test_url_var}"
        )
    return test_url_var


def env() -> str:
    """Returns the environment variable ENV value

    Defaults to production
    :returns: environment the app needs to run in"""
    env_var = getenv("ENV", "production")
    return env_var


def telegram() -> list[str]:
    """Returns all telegram environment variables
    [
        TELEGRAM_API_ID,
        TELEGRAM_API_HASH,
        TELEGRAM_BOT_TOKEN
    ]

    :returns: a list of telegram environment variables"""

    api_id = getenv("TELEGRAM_API_ID")
    api_hash = getenv("TELEGRAM_API_HASH")
    bot_token = getenv("TELEGRAM_BOT_TOKEN")

    if not api_id or not api_hash or not bot_token:
        raise EnvironmentError("All telegram env vars not set!")
    return [api_id, api_hash, bot_token]
