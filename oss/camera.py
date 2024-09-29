import cv2


def show(n: int = 0):
    '''
    打开本地相机
    '''
    with_open(n, show_frame)


def with_open(n: int = 0, fn: callable = None):
    '''
    打开摄像头
    @param fn: 传入处理图片函数,返回是否退出
    '''
    cap = cv2.VideoCapture(n)
    while True:
        ret, frame = cap.read()
        if ret:
            if fn(frame):
                break
    cap.release()
    cv2.destroyAllWindows()


def show_frame(frame, name='frame', quit='q'):
    '''
    显示图片
    @param frame: 图片
    @param name: 图片名
    @param quit: 退出键
    '''
    cv2.imshow(name, frame)
    return cv2.waitKey(1) & 0xFF == ord(quit)

