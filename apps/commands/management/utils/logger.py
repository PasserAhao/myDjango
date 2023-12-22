import sys
from django.core.management.base import OutputWrapper
from apps.commands.management.utils.config import CmdLogLevel, Color, PREFIX, LOG_LEVEL_MAP

color_level_map = {
    CmdLogLevel.INFO.value: Color.CYAN.value,
    CmdLogLevel.DEBUG.value: Color.PURPLE.value,
    CmdLogLevel.WARNING.value: Color.YELLOW.value,
    CmdLogLevel.ERROR.value: Color.RED.value
}


class CmdLog:
    def __init__(self, content, level):
        self.content = content
        self.level = level

    def __str__(self):
        return f"日志等级: {self.level}\n 日志信息: {self.content}"


class CmdLogger:

    def __init__(self, level, *args, **kwargs):
        self.level = LOG_LEVEL_MAP.get(level, 2)

    def _analyse_logs(self, log: CmdLog):
        """
        预留函数:
        打印的日志可能大多数是从各个组件返回的信息,又或者是一些警告,报错信息.
        而设置这个方法是认为这些信息是可以通过分析给出一些建议性的提示或者自愈操作.
        你可以通过这个方法对交互的日志进行简单处理, 又或者将日志转移到自定义的日志分析器进行更复杂的处理
        """
        pass

    def _printf(self, msgs, level=CmdLogLevel.INFO.value, color=None, stdout=None, stderr=None, prefix=True):
        is_err = True if level == CmdLogLevel.ERROR.value else False
        console = OutputWrapper((stderr or sys.stderr) if is_err else (stdout or sys.stdout))

        color = color or color_level_map.get(level)
        if iter(msgs):
            console.write("".join([self.color_msg(msg, color, prefix=prefix) for msg in msgs]))
            [self._analyse_logs(CmdLog(_msg, level)) for _msg in msgs]
            return
        console.write(self.color_msg(msgs, color, prefix=prefix))
        self._analyse_logs(CmdLog(msgs, level))

    def printf(self, msgs, level, *args, **kwargs):
        if self.level < LOG_LEVEL_MAP.get(level, 1):
            return
        self._printf(msgs, level, *args, **kwargs)

    @staticmethod
    def color_msg(msg, color=Color.CYAN.value, prefix=False):
        return f"{PREFIX if prefix else ''}{color}{msg}{Color.RESET.value}"

    def info(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.INFO.value, prefix=prefix)

    def error(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.ERROR.value, prefix=prefix)

    def waring(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.WARNING.value, prefix=prefix)

    def debug(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.DEBUG.value, prefix=prefix)
