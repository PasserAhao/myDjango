import redis
from django.conf import settings
from redis.sentinel import Sentinel

REDIS_CONNECTION_POOL = None
SENTINEL = None
MASTER = None
SINGLE_MASTER = None


class RedisError(Exception):
    """Redis错误类"""

    pass


class RedisConfError(RedisError):
    """Redis配置错误类"""

    pass


def _get_redis_conf():
    if not (settings.REDIS_HOST and settings.REDIS_PORT and settings.REDIS_DB and settings.REDIS_PASSWORD):
        raise RedisConfError("get redis conf error, please check your redis settings.")
    else:
        redis_conf = {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "db": settings.REDIS_DB,
            "password": settings.REDIS_PASSWORD,
        }
    if settings.REDIS_MODE.upper() == "SENTINEL" and not settings.REDIS_SERVICE_NAME:
        raise RedisConfError("get redis conf error, please check your redis settings.")
    else:
        redis_service_name = settings.REDIS_SERVICE_NAME

    return redis_conf, redis_service_name


def _get_redis_connection_pool():
    global REDIS_CONNECTION_POOL
    try:
        if REDIS_CONNECTION_POOL is None:
            redis_conf, _ = _get_redis_conf()
            REDIS_CONNECTION_POOL = redis.ConnectionPool(**redis_conf)
        return REDIS_CONNECTION_POOL
    except Exception as e:
        raise RedisError("get redis pool error, details: %s" % repr(e))


def _extract_sentinel_conf(redis_conf):
    sentinel_list = []
    host_str = redis_conf["host"]
    port_str = redis_conf["port"] or 6379
    password = redis_conf["password"] or ""
    db = redis_conf["db"] or 0

    host_list = host_str.split(",")
    port_list = port_str.split(",")
    if len(port_list) == len(host_list):
        for i, host in enumerate(host_list):
            sentinel_list.append((host, port_list[i]))
    else:
        for host in host_list:
            sentinel_list.append((host, port_list[0]))

    return sentinel_list, password, db


def get_redis_connection():
    connection = None

    if settings.REDIS_MODE == "SENTINEL":
        redis_conf, service_name = _get_redis_conf()
        sentinel_list, password, db = _extract_sentinel_conf(redis_conf)
        connection = get_redis_sentinel_connection(sentinel_list, service_name, password, db)

    if settings.REDIS_MODE == "SINGLE":
        connection = get_single_redis_connection()

    return connection


def get_single_redis_connection():
    global SINGLE_MASTER
    try:
        if SINGLE_MASTER is None:
            connection_pool = _get_redis_connection_pool()
            SINGLE_MASTER = redis.Redis(connection_pool=connection_pool, socket_timeout=settings.REDIS_TIMEOUT)
        return SINGLE_MASTER
    except Exception as e:
        raise RedisError("get redis connection error, details: %s" % repr(e))


def get_redis_sentinel_connection(sentinel_list, service_name, redis_password, db=1):
    """获取哨兵模式下的redis集群连接"""
    global SENTINEL
    global MASTER
    try:
        if SENTINEL is None:
            sentinel_kwargs = {"password": settings.SENTINEL_PASSWORD}
            SENTINEL = Sentinel(sentinel_list, socket_timeout=settings.REDIS_TIMEOUT, sentinel_kwargs=sentinel_kwargs)
        if MASTER is None:
            MASTER = SENTINEL.master_for(
                service_name=service_name, socket_timeout=settings.REDIS_TIMEOUT, password=redis_password, db=db
            )
        return MASTER
    except Exception as e:
        raise RedisError("get redis sentinel connection error, details: %s" % repr(e))
