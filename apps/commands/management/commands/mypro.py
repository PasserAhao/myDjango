from django.core.management.base import BaseCommand

from apps.commands.management.utils.logger import CmdLogger
from apps.commands.management.plugins.default import DefaultCommand


class Command(BaseCommand):
    help = "this is a test demo"

    def __init__(self):
        super().__init__()
        # todo 自动发现
        self.factory_map = {}

    def help(self):
        # todo 这里解释所有插件信息
        pass

    def add_arguments(self, parser):
        parser.add_argument("--level", nargs="?", type=str, help="日志等级")
        parser.add_argument("--interactive", action="store_true", help="开启快捷交互模式")
        parser.add_argument("--custom-help", action="store_true", help="显示插件所有可用方法以及注释")
        parser.add_argument("--plugin", type=str, default="default", help="选择要执行的插件")
        parser.add_argument("--list", action="store_true", help="展示所有的插件以及插件说明")

        parser.add_argument("args", nargs="*", type=str, help="执行函数参数")
        parser.add_argument("--root", action="store_true", help="是否允许操作危险操作")
        parser.add_argument("--func-help", action="store_true", help="显示某个方法的注释")

    def handle(self, *args, **options):
        if options.get("list"):
            self.help()
            return

        log = CmdLogger(options.get("level"))
        try:
            client = self.factory_map.get(options.get("plugin"), DefaultCommand)(log, config=options)
            if not options.get("interactive"):
                self.cmd_interactive(client, args)
                return
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            log.detail(error_detail)
            log.error(f"错误信息: {e}")

    def fast_interactive(self, client, ):
        pass

    @staticmethod
    def cmd_interactive(client, params):
        if not params:  # 没有任何参数的事情执行help方法
            params = ("help",)
        func_name, *func_args = params
        client.exec(func_name, func_args)
