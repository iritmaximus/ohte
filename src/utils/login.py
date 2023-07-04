import bcrypt


def create_password_hash(password: str) -> str:
    """Creates passwordhash for secure password saving

    :param password: cleartext password
    :returns: hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, password_hash: str) -> bool:
    """Checks if the password and the hash match

    :param password: cleartext password
    :param password_hash: hashed password that is checked
    :returns: bool, if the passwords match
    """

    return bcrypt.checkpw(password, password_hash)
