import threading
import time
import builtins

print_lock = threading.Lock()
default_format = "%Y-%m-%d %H:%M:%S:"


def print(*args, sep=' ', end='\n', file=None):
    print_lock.acquire()
    builtins.print(*args, sep=sep, end=end, file=file)
    print_lock.release()


def log(*args, sep=' ', end='\n', file=None, tag: str = "日志", format: str = default_format, color: int = 0):
    print(f'\x1b[0;{color}m[{tag}] {time.strftime(format)}', *args, '\x1b[0m', sep=sep, end=end, file=file)


def trace(*args, sep=' ', end='\n', file=None, tag: str = "追溯", format: str = default_format, color: int = 32):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)


def debug(*args, sep=' ', end='\n', file=None, tag: str = "调试", format: str = default_format, color: int = 33):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)


def read(*args, sep=' ', end='\n', file=None, tag: str = "读取", format: str = default_format, color: int = 37):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)


def write(*args, sep=' ', end='\n', file=None, tag: str = "写入", format: str = default_format, color: int = 37):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)


def info(*args, sep=' ', end='\n', file=None, tag: str = "信息", format: str = default_format, color: int = 34):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)


def warn(*args, sep=' ', end='\n', file=None, tag: str = "警告", format: str = default_format, color: int = 35):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)


def error(*args, sep=' ', end='\n', file=None, tag: str = "错误", format: str = default_format, color: int = 31):
    log(*args, sep=sep, end=end, file=file, tag=tag, format=format, color=color)
