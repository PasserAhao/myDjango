import sys

from django.core.management.base import OutputWrapper

from commands.management.utils.config import PREFIX, CmdLogLevel, Color

color_level_map = {
    CmdLogLevel.INFO: Color.CYAN,
    CmdLogLevel.DEBUG: Color.PURPLE,
    CmdLogLevel.WARNING: Color.YELLOW,
    CmdLogLevel.ERROR: Color.RED,
}


class CmdLog:
    def __init__(self, content, level):
        self.content = content
        self.level = level

    def __str__(self):
        return f"日志等级: {self.level}\n 日志信息: {self.content}"


class CmdLogger:
    def __init__(self, level, *args, **kwargs):
        self.level = getattr(CmdLogLevel, level.upper(), CmdLogLevel.INFO)

    def _analyse_logs(self, log: CmdLog):
        """
        预留函数:
        打印的日志可能大多数是从各个组件返回的信息,又或者是一些警告,报错信息.
        而设置这个方法是认为这些信息是可以通过分析给出一些建议性的提示或者自愈操作.
        你可以通过这个方法对交互的日志进行简单处理, 又或者将日志转移到自定义的日志分析器进行更复杂的处理
        """
        pass

    def _printf(self, msgs, level=CmdLogLevel.INFO, color=None, stdout=None, stderr=None, prefix=True):
        is_err = True if level == CmdLogLevel.ERROR else False
        console = OutputWrapper((stderr or sys.stderr) if is_err else (stdout or sys.stdout))

        color = color or color_level_map.get(level)
        result_msg = f"{PREFIX if prefix else ''}"
        if iter(msgs):
            result_msg += "".join([self.color_msg(msg, color) for msg in msgs])
            console.write(result_msg)
            [self._analyse_logs(CmdLog(_msg, level)) for _msg in msgs]
            return
        result_msg += self.color_msg(msgs, color)
        console.write(result_msg)
        self._analyse_logs(CmdLog(msgs, level))

    def printf(self, msgs, level, *args, **kwargs):
        if level < self.level:
            return
        self._printf(msgs, level, *args, **kwargs)

    @staticmethod
    def color_msg(msg, color=Color.CYAN):
        return f"{color}{msg}{Color.RESET}"

    def info(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.INFO, prefix=prefix)

    def error(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.ERROR, prefix=prefix)

    def waring(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.WARNING, prefix=prefix)

    def debug(self, *message, prefix=True):
        self.printf(message, CmdLogLevel.DEBUG, prefix=prefix)
