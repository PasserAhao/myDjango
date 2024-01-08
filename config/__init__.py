import os
import pymysql

pymysql.install_as_MySQLdb()


def get_env_or_raise(key):
    """Get an environment variable, if it does not exist, raise an exception"""
    value = os.environ.get(key)
    skip_ci_exception_raise = os.getenv("SKIP_CI_EXCEPTION_RAISE", 0)
    if not value and not int(skip_ci_exception_raise):
        raise RuntimeError(
            'Environment variable "{}" not found, you must set this variable to run this application.'.format(key)
        )
    return value


REDIS_HOST = get_env_or_raise("APP_REDIS_HOST")
REDIS_PORT = get_env_or_raise("APP_REDIS_PORT")
REDIS_SERVICE_NAME = os.environ.get("APP_REDIS_SERVICE_NAME", "master")
REDIS_DB = get_env_or_raise("APP_REDIS_DB")
REDIS_PASSWORD = get_env_or_raise("APP_REDIS_PASSWORD")
SENTINEL_PASSWORD = os.environ.get("APP_SENTINEL_PASSWORD", "")
REDIS_MODE = get_env_or_raise("APP_REDIS_MODE").upper() if get_env_or_raise("APP_REDIS_MODE") else "SINGLE"
REDIS_TIMEOUT = int(os.environ.get("APP_REDIS_TIMEOUT", "2"))
