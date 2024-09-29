import img.img

def img_show(im, name='img'):
    """
    显示图片
    """
    img.show(im, name)


def img_write_text(im, text, position, color=(0, 255, 0, 1), size=30, font_dir=''):
    """
    在图片上添加文字
    """
    img.write_text(im, text, position, color, size, font_dir)

