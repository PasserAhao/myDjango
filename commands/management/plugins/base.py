"""
编写新插件说明 !!!

插件为动态扫描加载, 请注意命名规范(  文件名 + Command (注意首字母大写) ) eg: DefaultCommand
为了方便使用请务必完成一下要求:
  - 一个py文件只写一个插件类
  - 插件类必须注释说明插件的作以及范围等信息
  - 每一个方法都必须在注释中说明方法作用, 参数等信息(注释必须体现传参顺序)

调用说明:
  - 查看所有可以使用插件
    · python manage.py bcmd --list
  - 查看某个插件的所有可执行方法:
    · python manage.py bcmd --plugin=default
    · python manage.py bcmd --plugin=default --custom-help
  - 执行插件中的某个方法(使用默认插件 所以可以取消 --plugin=default 参数)
    · 基本命令: python manage.py bcmd <方法名> [参数...] --plugin=<插件名 不传使用默认插件>
      eg:
        python manage.py bcmd demo xiaoming 26
        python manage.py bcmd demo name=xiaoming age=26
  - 查看某个方法的使用说明
    · python manage.py bcmd demo --func-help
  - 显示更详细的日志
    · python manage.py bcmd demo [...] --level=debug

"""
import functools
import inspect
import re

from commands.management.utils.common import value_format
from commands.management.utils.config import FUNC_SIMILARITY_SCORE, Color
from commands.management.utils.logger import CmdLogger


def options(flag, *args, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, func_name, params):
            if hasattr(self, f"_{flag}"):
                getattr(self, f"_{flag}")(func_name)

            func(self, func_name, params)
            return

        return wrapper

    return decorator


class CustomCommand:
    def __init__(self, logger: CmdLogger, config=None, *args, **kwargs):
        self.log = logger
        self._config = config
        self._default_exclude_func = ["handle_command", "run", "table_format", "get_similarity_func"]
        self.exclude_func = []

    @options("func_help", help="是否展示方法注释")
    def handle_command(self, func_name, params):
        func_args, func_kwargs = self.parser_args(params)
        exclude_funcs = {*self.exclude_func, *self._default_exclude_func}
        # 如果输入方法不存在, 则返回相似的方法
        if func_name in exclude_funcs or not hasattr(self, func_name):
            self.log.error(f"{self.__class__.__name__} object has no attribute '{func_name}'")
            self.get_similarity_func(func_name)
            return
        self.run(func_name, *func_args, **func_kwargs)

    def help(self):
        """
        查看可执行方法
        """
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

    def _get_methods_with_doc(self, obj=None):
        """
        获取对象中的所有方法以及注释说明
        :params obj: 类对象
        """
        exclude_func = [*self._default_exclude_func, *self.exclude_func]
        methods = inspect.getmembers(obj or self, predicate=inspect.ismethod)
        method_docs = {method[0]: inspect.getdoc(method[1]) for method in methods if not method[0].startswith("_")}

        [method_docs.pop(func) for func in exclude_func if method_docs.__contains__(func)]
        return method_docs

    @staticmethod
    def _get_function_parameters(func):
        """
        获取方法的固定参数和可选参数
        :params func: 方法名
        """
        signature = inspect.signature(func)
        parameters = signature.parameters
        required_params = []
        optional_params = []

        for param_name, param_info in parameters.items():
            if param_info.default == inspect.Parameter.empty:
                required_params.append(param_name)
            else:
                optional_params.append(param_name)

        return required_params, optional_params

    def get_similarity_func(self, func, obj=None, score=FUNC_SIMILARITY_SCORE):
        """
        获取某个类中与func相似的方法
        : params func: 方法名
        : params obj: 类对象
        : params score: 阈值, 该方法会返回相似度高于阈值的部分方法
        """
        has_funcs = self._get_methods_with_doc(obj)
        self.log.info(format("", "-^50"), prefix=False)
        for _func, doc in has_funcs.items():
            similarity = self._jaccard_similarity(func, _func)
            if similarity < score and func not in _func:
                continue
            self.log.info(f"方法名称: {_func}", prefix=False)
            self.log.info(f"使用说明: {doc}", prefix=False)
            self.log.info(format("", "-^50"), prefix=False)
        self.log.info(self.log.color_msg(f"未找到{func}方法, 为您找到以上相似方法...", Color.PURPLE.value))

    @staticmethod
    def _jaccard_similarity(str1, str2):
        """
        判断连个字符串的相似度
        :params str1: 字符串1
        :params str2: 字符串2
        """
        set1, set2 = set(str1), str(str2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        similarity = intersection / union if union != 0 else 0
        return similarity * 100

    def _func_help(self, func_name):
        """
        处理func-help 参数: 打印方法的注释说明
        """
        if not self._config.get("func_help"):
            return
        func_dic = self._get_methods_with_doc()
        if not func_dic.__contains__(func_name):
            self.log.error(f"type object '{self.__class__.__name__}' has no attribute '{func_name}'")
            return
        self.log.info(func_dic.get(func_name))
        return

    def table_format(self, headers, datas):
        _compile = re.compile("\x1B\\[\\d+m(.*)\x1B\\[\\d+m")

        def has_color_escape_code(input_str):
            # 使用正则表达式来检查字符串中是否包含 ANSI 转义序列
            ansi_escape_pattern = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
            return bool(ansi_escape_pattern.search(str(input_str)))

        def data_row(row, cws):
            body_data = []
            join_str = self.log.color_msg("|")
            for idx, cell in enumerate(row):
                alignment = "<" if idx == 0 else "^"
                if has_color_escape_code(cell):
                    num = len(cell) - len(_compile.search(cell).group(1))
                    body_data.append(format(cell, f"{alignment}{cws[idx] + num}"))
                    continue
                body_data.append(self.log.color_msg(format(cell, f"{alignment}{cws[idx]}")))
            return join_str + f"{join_str * 2}".join(body_data) + join_str

        def _len(string):
            return len(_compile.search(string).group(1)) if has_color_escape_code(string) else len(string) + 2

        # 找出每列的最大宽度
        column_widths = []
        for i in range(len(headers)):
            column_widths.append(max(_len(str(row[i])) for row in datas + [headers]))
        halving_line = "+" + "++".join([f"{'-' * num}" for num in column_widths]) + "+"
        # 打印上边框
        self.log.info(halving_line, prefix=False)
        # 打印表头
        self.log.info(data_row(headers, column_widths), prefix=False)
        # 打印分隔线
        self.log.info(halving_line, prefix=False)
        # 打印数据行
        [self.log.info(data_row(row, column_widths), prefix=False) for row in datas]
        # 打印下边框
        self.log.info(halving_line, prefix=False)

    def demo(self, name, age, *args, **kwargs):
        """
        请注意每个方法务必写清楚其作用, 参数(是否必填,默认值等), 返回值, 以及执行后可能受到的影响等等
        eg:
            这是一个demo方法, 作用是打印一个人的年龄信息
            :param name (必填): 人的名字
            :param age (非必填): 人的年龄 默认值 12
            :return: 返回一个人的实例
        """

        class People:
            def __init__(self, _name, _age):
                self.name = _name
                self.age = _age

        self.log.info(f"{name} 今年 {age}岁了")
        return People(name, age)
