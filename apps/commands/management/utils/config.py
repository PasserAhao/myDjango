from enum import Enum


class Color(Enum):
    # 重置所有文本样式
    RESET = "\033[0m"
    # 不同颜色的 ANSI 转义码
    RED = "\033[31m"  # 红色
    GREEN = "\033[32m"  # 绿色
    YELLOW = "\033[33m"  # 黄色
    BLUE = "\033[34m"  # 蓝色
    PURPLE = "\033[35m"  # 紫色
    CYAN = "\033[36m"  # 青色
    WHITE = "\033[37m"  # 白色


class CmdLogLevel(Enum):
    INFO = "info"
    DETAIL = "detail"
    REMIND = "remind"
    WARNING = "warning"
    ERROR = "error"


# 交互日志等级数值
LOG_LEVEL_MAP = {
    CmdLogLevel.INFO.value: 2,
    CmdLogLevel.ERROR.value: 0,  # 这里的错误是交互模式中很重要的一个信息反馈, 必须展示
    CmdLogLevel.WARNING.value: 1,
    CmdLogLevel.REMIND.value: 3,
    CmdLogLevel.DETAIL.value: 4,  # 这里才是正常情况下理解的error的内容
}

# 交互日志前缀
PREFIX = ">>> "
