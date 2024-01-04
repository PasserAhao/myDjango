import json
import requests
from commands.management.utils.config import Color, COLOR_SPLIT
from commands.management.plugins.base import ConstCommand

"""
编写新插件说明 !!!

插件为动态扫描加载, 请注意命名规范(  文件名 + Command (注意首字母大写) ) eg: DefaultCommand
为了方便使用请务必完成一下要求:
  - 一个py文件只写一个插件类
  - 插件类必须注释说明插件的作以及范围等信息
  - 每一个方法都必须在注释中说明方法作用, 参数等信息(注释必须体现传参顺序)

调用说明:
  使用demo方法:
    python manage.py kac_admin demo xiaoming 26
  如果非默认插件
    python manage.py kac_admin demo xiaoming 56 --plugin=<your plugin name>
  关键字传参:
    python manage.py kac_admin demo age=56 name=xiaoming
  关键字和普通参数传参(需要注意普通参数需要依照传参顺序传参)
    比如func的参数为: func(arg1, arg2, arg3)
    传参为: 52 arg1=56 sss
    解释: 52 sss 两个普通参数会优先给 arg1 arg2 此时关键字参数还给arg1 或者 arg2 赋值就会报错
"""


class DefaultCommand(ConstCommand):
    """
    这里是常用的一些命令方法集
    """

    def __init__(self, log, config):
        super().__init__(log, config)
        self.exclude_func = []
        self.last_rmq_details = {}

    def run(self, func, *args, **kwargs):
        getattr(self, func)(*args, **kwargs)

    def rely_health_check(self):
        pass

    def rabbitmq_queues_info(self):
        """
        获取rabbitmq队列详情信息
        :param 无
        """
        # todo 使用redis缓存上一次数据, 然后根据
        res = requests.get(url='http://localhost:25672/api/queues', auth=('guest', 'guest'))
        aa = json.loads(res.content.decode())
        headers = ['name', 'state', 'messages', 'ready', 'unacknowledged', 'consumers']
        table_data = []
        red_str = lambda s: f"{s}{COLOR_SPLIT}{Color.RED.value}"
        for row in aa:
            name = row["name"]
            state = row["state"]
            messages = row["messages"]
            ready = row["messages_ready"]
            ready = ready if int(ready) < 2 else red_str(ready)
            unacknowledged = row["messages_unacknowledged"]
            consumers = row["consumers"]
            row_data = [
                name, state, messages, ready, unacknowledged, consumers
            ]
            table_data.append(row_data)
        self.table_format(headers, table_data)

    def demo(self, name, age, *args, **kwargs):
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
        infos = [
            f"{name}{self.log.color_msg(age, color=Color.RED.value)}",
            f"{name}{self.log.color_msg(name, color=Color.BLUE.value)}"
        ]
        self.log.info(*infos)
        return People(name, age)