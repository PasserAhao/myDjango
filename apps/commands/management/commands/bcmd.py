import os
import importlib as _imp
import importlib.util

from django.core.management.base import BaseCommand

from apps.commands.management.utils.logger import CmdLogger
from apps.commands.management.plugins.default import DefaultCommand


def dynamic_plugins_importer(path: str) -> dict:
    base_path = os.path.dirname(os.path.dirname(__file__))
    plugin_path = os.path.join(base_path, "plugins")  # 构建插件路径

    modules_inst_map = {}
    files = os.listdir(path)
    for file in files:
        if file.startswith("_") or not file.endswith(".py"):
            continue
        module_name = file[:-3]  # 提取模块名（去除文件扩展名 .py）
        file_path = os.path.join(plugin_path, file)  # 构建文件的完整路径

        # 使用 importlib.util 动态导入模块
        spec = _imp.util.spec_from_file_location(module_name, file_path)
        module = _imp.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # 将module加载到内存中使用
        class_obj = f"{module_name.capitalize()}Command"
        if hasattr(module, class_obj):
            modules_inst_map[module_name] = getattr(module, class_obj)
    return modules_inst_map


class Command(BaseCommand):
    help = "一个命令集框架, 可以在这里丰富更多的自定义命令"

    def __init__(self):
        super().__init__()
        plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
        self.factory_map = dynamic_plugins_importer(plugin_dir)

    def help(self, log: CmdLogger):
        for module_name, module in self.factory_map.items():
            log.info(format(f"插件名称: {module_name}", "-^80"), prefix=False)
            log.info(f"说明: {module.__doc__}", prefix=False)
        log.info(format("", "-^84"), prefix=False)

    def add_arguments(self, parser):
        parser.add_argument("args", nargs="*", type=str, help="执行函数参数")

        parser.add_argument("--level", nargs="?", type=str, help="日志等级")
        parser.add_argument("--interactive", action="store_true", help="开启快捷交互模式")
        parser.add_argument("--custom-help", action="store_true", help="显示插件所有可用方法以及注释")
        parser.add_argument("--plugin", type=str, default="default", help="选择要执行的插件")
        parser.add_argument("--list", action="store_true", help="展示所有的插件以及插件说明")

        parser.add_argument("--func-help", action="store_true", help="显示某个方法的注释")

    def handle(self, *args, **options):
        log = CmdLogger(options.get("level"))

        if options.get("list"):
            self.help(log)
            return
        try:
            client = self.factory_map.get(options.get("plugin"), DefaultCommand)(log, config=options)
            if not options.get("interactive"):
                self.cmd_interactive(client, args)
                return
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            log.debug(error_detail)
            log.error(f"错误信息: {e}")

    def fast_interactive(self, client, ):
        pass

    @staticmethod
    def cmd_interactive(client, params):
        if not params:  # 没有任何参数的事情执行help方法
            params = ("help",)
        func_name, *func_args = params
        client.handle_command(func_name, func_args)
