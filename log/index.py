import logging


# 定义彩色日志格式
class ColoredFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        # 设置不同级别的颜色代码
        self._fmt = {
            logging.DEBUG: "\033[0;37m%(asctime)s [%(levelname)s] %(message)s\033[0m",
            logging.INFO: "\033[0;32m%(asctime)s [%(levelname)s] %(message)s\033[0m",
            logging.WARNING: "\033[0;33m%(asctime)s [%(levelname)s] %(message)s\033[0m",
            logging.ERROR: "\033[0;31m%(asctime)s [%(levelname)s] %(message)s\033[0m",
            logging.CRITICAL: "\033[0;35m%(asctime)s [%(levelname)s] %(message)s\033[0m",
        }

    def format(self, record):
        log_fmt = self._fmt.get(record.levelno, self._fmt[logging.DEBUG])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# 创建 logger 对象
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
# 创建文件处理器
file_handler = logging.FileHandler('example.log')

# 创建彩色日志格式化程序
formatter = ColoredFormatter()

# 设置处理器的格式化程序
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到 logger 对象
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def critical(msg):
    logger.critical(msg)
