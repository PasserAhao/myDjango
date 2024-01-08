from baseserver.management.plugins.base import CustomCommand


class DefaultCommand(CustomCommand):
    """
    这里是常用的一些命令方法集
    """

    def __init__(self, log, config):
        super().__init__(log, config)
        self.exclude_func = []
        self.last_rmq_details = {}

    def demo(self, *args, **kwargs):
        from baseserver.common.redis_utils import get_redis_connection
        redis = get_redis_connection()
        redis.set("name", "asdasd")
        print(redis.get("name"))
