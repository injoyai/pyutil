import cv2
import threading


class Camera:
    def __init__(self, num: int = 0, middle: callable = None, last: callable = None):
        self.handler_last = last
        self.handler_last_run = False
        self.handler_last_lock = threading.Lock()
        self.handler_middle = middle
        self.num = num

    def run(self):
        cap = cv2.VideoCapture(self.num)
        while True:
            ret, frame = cap.read()
            if ret:
                self.__run_last(frame)
                if self.__run_middle(frame):
                    break
        cap.release()
        cv2.destroyAllWindows()

    def __run_middle(self, frame):
        if self.handler_middle is not None:
            return self.handler_middle(frame)
        return True

    def __run_last(self, frame):
        """
        看处理函数是否在运行,不在运行则开始使用线程处理,加锁,一次只允许一个线程运行
        """

        def run_last(frame):
            self.handler_last_run = True
            if self.handler_last is not None:
                self.handler_last(frame)
            self.handler_last_run = False

        self.handler_last_lock.acquire()
        if not self.handler_last_run:
            threading.Thread(target=run_last, args=(frame,)).start()
        self.handler_last_lock.release()
