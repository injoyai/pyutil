import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import oss

import g


def show(im=None, name='img'):
    """
    显示图片
    """
    if im is None or not g.is_windows():
        return
    name = str(name)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
    cv2.resizeWindow(name, im.shape[1], im.shape[0])
    # 显示图片 ('名称','图片')
    cv2.imshow(name, im)
    # 等待键盘输入 毫秒(0表示无限等待) , 按任意键跳过
    cv2.waitKey(1)  # 1 millisecond


def write_text(img, text, position, color=(0, 255, 0, 1), size=30, font_dir=''):
    """
    给图片增加文本
    """
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    img = img.convert('RGBA')
    # 字体的格式
    font_style = None
    if oss.path.exists(font_dir):
        font_style = ImageFont.truetype(font_dir, size, encoding="utf-8")

    # 绘制文本
    mark = Image.new('RGBA', img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(mark)
    d.text(position, text, color, font=font_style)
    img = Image.alpha_composite(img, mark)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def resize_square(im):
    # 改变图片大小

    # 获取图片的宽度和高度
    height, width = im.shape[0],im.shape[1]

    # 计算裁剪或填充后的正方形边长
    target_size = max(width, height)

    # 创建一个白色底色的新图像
    square_img = 255 * np.ones((target_size, target_size, 3), dtype=np.uint8)

    # 计算将图片居中放置时的起始坐标
    x_offset = (target_size - width) // 2
    y_offset = (target_size - height) // 2

    # 将原始图片复制到正方形图像中
    # square_img[y_offset:y_offset + height, x_offset:x_offset + width, :] = im

    # 调整大小（如果需要）
    square_img = cv2.resize(square_img, (128, 128), interpolation=cv2.INTER_AREA)

    return square_img
