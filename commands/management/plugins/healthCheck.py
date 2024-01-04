from commands.management.plugins.base import ConstCommand


class HealthCheckCommand(ConstCommand):
    def __init__(self, log, config):
        super().__init__(log, config)
        self.exclude_func = []
