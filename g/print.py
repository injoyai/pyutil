import threading

print_lock = threading.Lock()


def println(*args):
    print_lock.acquire()
    print(*args)
    print_lock.release()
