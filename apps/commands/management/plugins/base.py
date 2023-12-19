import json
import inspect
import functools
from apps.commands.management.utils.logger import CmdLogger


def options(flag, *args, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, func_name, params):
            is_next = False
            if hasattr(self, f"_{flag}"):
                is_next = getattr(self, f"_{flag}")(func_name)
            if not is_next:
                return
            result = func(self, func_name, params)
            return result

        return wrapper

    return decorator


class MyBaseCommand:
    def __init__(self, logger: CmdLogger, config=None, *args, **kwargs):
        self.log = logger
        self.config = config
        self._default_exclude_func = ["exec", "run", "verify"]
        self.exclude_func = []
        self.root_func = ["demo"]  # 这里记录下危险操作, 执行时必须带上 +root 参数

    @options("root", help="是否校验方法有权限操作")
    @options("func_help", help="是否展示方法注释")
    def exec(self, func_name, params):
        func_args, func_kwargs = self.parser_args(params)
        code, msg = self.verify(*func_args, **func_kwargs)
        if code:
            self.log.error(f"参数校验错误, 错误详情:{msg}")
            return
        self.run(func_name, *func_args, **func_kwargs)

    def help(self):
        for func, describe in self._get_methods_with_doc().items():
            self.log.info(f"方法名称: {func}", f"方法注释: {describe}", prefix=False)
            self.log.info(format("", "-^50"), prefix=False)
        self.log.waring("可能涉及危险操作, 请谨慎操作!!!")

    @staticmethod
    def parser_args(params):
        func_args, func_kwargs = list(), dict()
        for param in params:
            if "=" in param:
                key, value = param.split("=")
                func_kwargs[key] = json.loads(value)
                continue
            func_args.append(json.loads(param))
        return func_args, func_kwargs

    @staticmethod
    def verify(*func_args, **func_kwargs) -> bool:
        code, msg = 0, "OK"
        return code, msg

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
        if not self.config.get("func_help"):
            return True
        func_dic = self._get_methods_with_doc()
        if not func_dic.__contains__(func_name):
            self.log.error(f"type object '{self.__class__.__name__}' has not attribute '{func_name}'")
            return False
        self.log.info(func_dic.get(func_name), "")
        return False

    def _root(self, func_name):
        if func_name in self.root_func and not self.config.get("root"):
            self.log.error(f"{func_name} 涉及危险操作, 请使用root操作.   你可以使用 --root 开启root权限")
            return False
        return True
