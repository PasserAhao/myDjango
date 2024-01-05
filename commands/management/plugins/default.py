from commands.management.plugins.base import CustomCommand


class DefaultCommand(CustomCommand):
    """
    这里是常用的一些命令方法集
    """

    def __init__(self, log, config):
        super().__init__(log, config)
        self.exclude_func = []
        self.last_rmq_details = {}
