import threading


class Lock:
    def __init__(self):
        self._lock = threading.Lock()
        pass

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()
