from enum import Enum, IntEnum


class Color(Enum):
    def __str__(self):
        return self.value

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


class CmdLogLevel(IntEnum):
    INFO = 2
    DEBUG = 1
    WARNING = 3
    ERROR = 10


# 交互日志前缀
PREFIX = ">>> "

# cmd 信息缓存key
COMMAND_CACHE_KEY = "command_cache_key"

# 方法相似度阈值
FUNC_SIMILARITY_SCORE = 60
