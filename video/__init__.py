import video.camera
import cv2


def show_frame(frame, name='frame', quit='q'):
    """
    显示图片
    @param frame: 图片
    @param name: 图片名
    @param quit: 退出键
    """
    cv2.imshow(name, frame)
    return cv2.waitKey(1) & 0xFF == ord(quit)


def with_open(source, middle: callable = show_frame, last: callable = None):
    if type(source) == int:
        with_open_camera(source, middle, last)
    else:
        return


def with_open_camera(n: int = 0, middle: callable = None, last: callable = None):
    """
    打开摄像头,会等待回调函数处理完成后再读取下一帧
    如果处理速度过慢,则会导致摄像头卡住
    @param n: 摄像头编号
    @param middle: 传入处理图片函数,返回是否退出
    @param last: 线程执行,取最新一帧
    """
    camera.Camera(n, middle, last).run()
