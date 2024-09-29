import struct
import subprocess
import time
import cv2
import g
import g.struct as st


class Writer:
    """
    通过ffmpeg推送视频流
    """

    def __init__(self, rtmp_url, fps=30, width=640, height=480, retry_interval=5):
        self.last_connect = time.time()
        self.rtmp_url = rtmp_url
        self.fps = fps
        self.width = width
        self.height = height
        self.retry_interval = retry_interval
        # 创建FFmpeg命令行参数
        ffmpeg_cmd = ['ffmpeg',
                      '-y',
                      '-f', 'rawvideo',
                      '-vcodec', 'rawvideo',
                      '-pix_fmt', 'bgr24',
                      '-s', "{}x{}".format(width, height),
                      '-r', str(fps),
                      '-i', '-',
                      '-c:v', 'libx264',
                      '-pix_fmt', 'yuv420p',
                      '-preset', 'ultrafast',
                      '-f', 'flv',
                      rtmp_url]
        print('ffmpeg_cmd:', ffmpeg_cmd)
        try:
            # 启动 ffmpeg
            self.ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
        except (OSError, TypeError, NameError) as err:
            print('subprocess_err:', err)

    def write(self, im):
        if im is None:
            return
        try:
            self.ffmpeg_process.stdin.write(im.tobytes())
        except (OSError, TypeError, NameError) as err:
            print('push_err:', err)
            if time.time() - self.last_connect > self.retry_interval:
                self.__init__(self.rtmp_url, self.fps, self.width, self.height)


class Reader:
    def __init__(self, source):
        self._last = g.Last()
        self.lasts = [self._last]

        _source=source
        if source == str(int(_source)):
            _source = int(_source)
        cap = cv2.VideoCapture(_source)
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        def read(cap, source):
            while cap.isOpened():
                # cap.grab() 这个开启推流有时会花屏
                ret, im = cap.read()
                if ret and im is not None:
                    for c in self.lasts:
                        c.set(im)
                time.sleep(0.0)

        g.go(read, args=(cap, source))

    def __iter__(self):
        return self

    def __next__(self):
        return self._last.get_new()

    def last(self):
        c = g.Last()
        self.lasts.append(c)
        return c

    def listen(self, fn):
        """
        监听数据,并执行fn,参数为im
        """

        def _fn():
            for im in self.last():
                fn(im)

        g.go(_fn)


class Readers:
    def __init__(self, sources: list):
        self.readers = {}
        for key, source in enumerate(sources):
            self.readers[key] = Reader(source)
        self._lasts = self.lasts()

    def __iter__(self):
        return self

    def __next__(self):
        return self._lasts.__next__()

    def lasts(self):
        lasts = {}
        for key, reader in dict.items(self.readers):
            lasts[key] = reader.last()
        return st.Lasts(lasts)

    def listen(self, fn):
        def _fn():
            for ims in self.lasts():
                for key, im in dict.items(ims):
                    fn(key, im)

        g.go(_fn)
