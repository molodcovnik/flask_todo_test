import bcrypt


def generate_hash(password: str):
    password_bytes = password.encode("utf-8")
    password_salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, password_salt)
    hash_str = hash_bytes.decode("utf-8")

    return hash_str


def authenticate(password, hash):
    password_bytes = password.encode("utf-8")
    hash_bytes = hash.encode("utf-8")
    result = bcrypt.checkpw(password_bytes, hash_bytes)
    return result