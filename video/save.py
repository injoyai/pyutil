import os
import cv2


class Save:
    def __init__(self, filename='output.mp4', fourcc='mp4v', fps: int = 30, w=640, h=480, split: int = 150, number=-1):
        dir, name = os.path.split(filename)
        if len(dir) > 0 and not os.path.exists(dir):
            os.mkdir(dir)
        self.filename = filename
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.w = w
        self.h = h
        self.split = split
        self.writer = None
        self.closed = False
        self.current = 0
        self.index = 0
        self.number = number

    def __call__(self, *args, **kwargs):
        return self.write(*args, **kwargs)

    def write(self, frame):
        if self.closed:
            return False
        if self.index >= self.number > 0:
            self.close()
            return False
        if self.writer is None:
            dir, name = os.path.split(self.filename)
            filename = os.path.join(dir, f'{self.index}_{name}')
            self.writer = cv2.VideoWriter(filename, self.fourcc, self.fps, (self.w, self.h))
            self.index += 1
        self.writer.write(frame)
        self.current += 1
        if self.current >= self.split > 0:
            self.writer.release()
            self.writer = None
            self.current = 0
        return True

    def close(self):
        self.writer.release()
        self.closed = True


class Limit(Save):
    def __init__(self, limit: int, filename='output.mp4', fourcc='mp4v', fps: int = 30, w=640, h=480):
        super().__init__(filename, fourcc, fps, w, h, limit)


class Time(Save):
    def __init__(self, time: float, filename='output.mp4', fourcc='mp4v', fps: int = 30, w=640, h=480, ):
        super().__init__(filename, fourcc, fps, w, h, int(time * fps))
