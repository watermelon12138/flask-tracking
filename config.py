from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'flask-tracking.db')
    SQLALCHEMY_ECHO = False
    HASH_ROUNDS = 100000


class TestConfiguration(BaseConfiguration):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')
    # 把SQLite放到内存中，this way for running test quickly
    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1  # how many times a user’s password should be hashed before it is stored.


class DebugConfiguration(BaseConfiguration):
    DEBUG = True
