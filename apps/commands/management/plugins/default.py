from apps.commands.management.plugins.base import MyBaseCommand

"""
编写新插件说明 !!!

插件为动态扫描加载, 请注意命名规范(  文件名 + Command (注意首字母大写) ) eg: DefaultCommand
为了方便使用请务必完成一下要求:
  - 一个py文件只写一个插件类
  - 插件类必须注释说明插件的作以及范围等信息
  - 每一个方法都必须在注释中说明方法作用, 参数等信息
"""


class DefaultCommand(MyBaseCommand):
    """
    这里是常用的一些命令方法集
    """

    def __init__(self, log, config):
        super().__init__(log, config)
        self.exclude_func = ["default"]
        self.root_func = []

    def demo(self, name, age=12, *args, **kwargs):
        """
        请注意每个方法务必写清楚其作用, 参数(是否必填,默认值等), 返回值, 以及执行后肯呢个收到的影响
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
