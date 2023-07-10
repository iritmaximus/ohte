import bcrypt


def create_password_hash(password: str) -> str:
    """Creates passwordhash for secure password saving

    There is a bit of str + decode magic going on. That is because
    I wanted the output to be a str to avoid confusion later on
    about the type.

    * get b'pas5w0rDha5h' as a byte from hashpw()
    * decode the b'' out
    * stringify the result and return

    Checking the value later
    * you can stringify again
    * decode back into b''
    * use


    :param password: cleartext password
    :returns: hashed password
    :raises TypeError: if no password is given
    """
    password = str(password)
    return str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())


def check_password(password: str, password_hash: str) -> bool:
    """Checks if the password and the hash match

    :param password: cleartext password
    :param password_hash: hashed password that is checked
    :returns: bool, if the passwords match
    """

    password = str(password)
    return bcrypt.checkpw(password.encode(), str(password_hash).encode())
