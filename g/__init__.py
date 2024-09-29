import threading
import platform
from time import sleep as _sleep
import g.chan
import g.print as p
import g.ffmpeg
import g.lock


def println(*args):
    """
    按顺序打印,避免出现语句混乱的情况
    """
    p.println(*args)


def lock():
    """
    获取锁
    """
    return lock.Lock()


def go(fn, args=()):
    """
    快速开启线程,参考go的命名
    @param fn: 执行函数
    @param args: 执行函数的参数
    """
    threading.Thread(target=fn, args=args).start()


def go_interval(fn, sec=1.0, num=-1):
    """
    线程间隔执行函数
    """
    go(interval, args=(fn, sec, num))


def interval(fn, sec=1.0, num=-1):
    """
    间隔执行函数
    @param fn: 执行函数
    @param sec: 间隔秒数
    @param num: 间隔次数,负数为无限
    """
    if num < 0:
        n = 0
        while True:
            fn(n)
            sleep(sec)
            n += 1
    else:
        for n in range(num):
            fn(n)
            sleep(sec)


def do_nothing():
    """
    什么也不做
    """
    pass


def do(fn: staticmethod, args=()):
    fn(args)


def do_after(fn: staticmethod, args=(), sec=0.0):
    after(sec)
    fn(args)


def go_do_after(fn: callable, args=(), sec=0.0):
    go(do_after, args=(fn, args, sec))


def sleep(sec=1.0):
    """
    睡眠,秒
    """
    _sleep(sec)


def sleep_mill(mill=1.0):
    """
    睡眠,毫秒
    """
    _sleep(0.0001 * mill)


def after(sec=1.0):
    return sleep(sec)


def is_windows():
    """
    判断当前系统环境是否是windows
    """
    return platform.system() == 'Windows'


class Chan(chan.Chan):
    """
    模仿go的 chan ,
    使用sleep循环实现,
    可能会有1毫秒延迟
    """
    pass


def select(*args: (chan.Chan, callable), default: callable = None):
    """
    模仿go的select
    从多个chan读取数据
    """
    return chan.select(*args, default=default)


def for_select(*args: (chan.Chan, callable), default: callable = None):
    """
    循环select
    从多个chan读取数据
    """
    return chan.ForSelect(*args, default=default)


def ffmpeg_to_ts(old_name, new_name):
    """
    使用ffmpeg把视频转ts
    """
    ffmpeg.to_ts(old_name, new_name)
