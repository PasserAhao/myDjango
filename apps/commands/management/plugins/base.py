import inspect
import functools
from apps.commands.management.utils.common import value_format
from apps.commands.management.utils.logger import CmdLogger


def options(flag, *args, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, func_name, params):
            is_next = False
            if hasattr(self, f"_{flag}"):
                is_next = getattr(self, f"_{flag}")(func_name)
            if not is_next:
                return None
            result = func(self, func_name, params)
            return result

        return wrapper

    return decorator


class ConstCommand:
    def __init__(self, logger: CmdLogger, config=None, *args, **kwargs):
        self.log = logger
        self._config = config
        self._default_exclude_func = ["handle_command", "run"]
        self.exclude_func = []

    @options("func_help", help="是否展示方法注释")
    def handle_command(self, func_name, params):
        func_args, func_kwargs = self.parser_args(params)
        self.run(func_name, *func_args, **func_kwargs)

    def help(self):
        for func, describe in self._get_methods_with_doc().items():
            self.log.info(format(f"方法名称: {func}", "-^80"), prefix=False)
            self.log.info(f"\n{describe}\n", prefix=False)
        self.log.info(format("", "-^84"), prefix=False)
        self.log.waring("可能涉及危险操作, 请谨慎操作!!!")

    @staticmethod
    def parser_args(params):
        func_args, func_kwargs = list(), dict()
        for param in params:
            if "=" in param:
                key, value = param.split("=")
                func_kwargs[key] = value_format(param)
                continue
            func_args.append(value_format(param))
        return func_args, func_kwargs

    def run(self, func, *args, **kwargs):
        getattr(self, func)(*args, **kwargs)

    def init(self, *args, **kwargs):
        """
        初始化插件操作
        """
        raise ImportError(f"type object '{self.__class__.__name__}' has no attribute 'init'")

    def _get_methods_with_doc(self):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        method_docs = {
            method[0]: inspect.getdoc(method[1])
            for method in methods
            if not method[0].startswith("_") or method[0] in self.exclude_func
        }
        exclude_func = [*self._default_exclude_func, *self.exclude_func]
        [method_docs.pop(func) for func in exclude_func if method_docs.__contains__(func)]
        return method_docs

    def _func_help(self, func_name):
        if not self._config.get("func_help"):
            return True
        func_dic = self._get_methods_with_doc()
        if not func_dic.__contains__(func_name):
            self.log.error(f"type object '{self.__class__.__name__}' has not attribute '{func_name}'")
            return False
        self.log.info(func_dic.get(func_name), "")
        return False
