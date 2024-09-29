import queue
import time

import g


class Chan:
    def __init__(self, cap=0):
        self.cap = cap
        if self.cap <= 0:
            self.cap = 1
        self.index = 0
        self.queue = queue.Queue(self.cap)

    def __iter__(self):
        self.index += 1
        return self

    def __next__(self):
        self.get()

    def cap(self):
        return self.cap

    def append(self, data, default: staticmethod = None):
        if self.queue.full() and default is not None:
            default()
            return False
        self.queue.put(data)

        return True

    def get(self, default: callable = None):
        if self.queue.empty() and default is not None:
            default()
            return None, False
        return self.queue.get(), True

    def close(self):
        # todo 如何进行关闭和释放内存
        pass


def select(*args: (Chan, callable), default: callable = None):
    """
    模仿go的select
    从多个chan读取数据
    """

    while True:
        get = False  # 获取到数据
        val = None  # 获取到的数据
        for c in args:
            if isinstance(c, Chan):
                if get:
                    # 获取到数据,但是未设置处理函数,则退出不处理
                    return val

                data, has = c.get(g.do_nothing)
                if has:
                    get = True
                    val = data
            elif c is not None and get:
                return c(val)

        if default is not None:
            return default(None)

        # todo 如何优化?
        time.sleep(0.001)


class ForSelect:
    def __init__(self, *args: (Chan, callable), default: staticmethod):
        self.chans = args
        self.default = default

    def __iter__(self):
        return self

    def __next__(self):
        return select(*self.chans, default=self.default)
