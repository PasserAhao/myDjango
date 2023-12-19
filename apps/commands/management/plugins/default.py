from apps.commands.management.plugins.base import MyBaseCommand


class DefaultCommand(MyBaseCommand):
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
