import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 日志记录器名称（通常使用 __name__）

    Returns:
        配置好的 logger
    """
    logger = logging.getLogger(name)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 控制台 handler - 输出到 stdout（不影响 UI Console）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # 格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
