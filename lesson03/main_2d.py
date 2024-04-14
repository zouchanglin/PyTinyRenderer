import sys

from image import MyImage
from obj import OBJFile
from vector import Vec3, Vec2

def line(x0, y0, x1, y1, image, color):
    steep = False
    if abs(x0 - x1) < abs(y0 - y1):  # 如果线段很陡，我们转置图像
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:  # 确保线段是从左往右绘制
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    slope = 2 * dy
    step = 0

    y = y0

    y_incr = 1 if y1 > y0 else -1
    if steep:
        for x in range(x0, x1 + 1):
            image.putpixel((y, x), color)
            step += slope
            if step > dx:
                y += y_incr
                step -= 2 * dx
    else:
        for x in range(x0, x1 + 1):
            image.putpixel((x, y), color)
            step += slope
            if step > dx:
                y += y_incr
                step -= 2 * dx


white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def triangle_area_2d(a: Vec2, b: Vec2, c: Vec2):
    """
    计算三角形面积
    """
    return .5 * ((b.y - a.y) * (b.x + a.x) + (c.y - b.y) * (c.x + b.x) + (a.y - c.y) * (a.x + c.x))


def barycentric(A, B, C, P):
    """
    计算重心坐标 u, v, w
    """
    total_area = triangle_area_2d(A, B, C)
    if total_area == 0:
        return None  # 或者抛出一个异常，或者返回一个特殊的值
    u = triangle_area_2d(P, B, C) / total_area
    v = triangle_area_2d(P, C, A) / total_area
    w = triangle_area_2d(P, A, B) / total_area
    return Vec3([u, v, w])


def triangle(p0: Vec2, p1: Vec2, p2: Vec2, img: MyImage, color):
    min_x = max(0, min(p0.x, p1.x, p2.x))
    max_x = min(img.width - 1, max(p0.x, p1.x, p2.x))
    min_y = max(0, min(p0.y, p1.y, p2.y))
    max_y = min(img.height - 1, max(p0.y, p1.y, p2.y))
    P = Vec2((0, 0))
    # 遍历包围盒内的每个像素
    for P.y in range(min_y, max_y + 1):
        for P.x in range(min_x, max_x + 1):
            # 计算当前像素的重心坐标
            bc_screen = barycentric(p0, p1, p2, P)
            if bc_screen is None:
                continue
            # 如果像素的重心坐标的任何一个分量小于0，那么这个像素就在三角形的外部，我们就跳过它
            if bc_screen.x < 0 or bc_screen.y < 0 or bc_screen.z < 0:
                continue
            image.putpixel((P.x, P.y), color)


def rasterize(p0: Vec2, p1: Vec2, img: MyImage, y_img: MyImage, color, buffer):
    if p0.x > p1.x:
        p0, p1 = p1, p0
    for x in range(p0.x, p1.x + 1):
        _x = p1.x - p0.x
        if _x == 0:
            continue
        # 计算线性插值的参数
        t = (x - p0.x) / _x
        # 对 y 值进行线性插值
        y = int(p0.y * (1 - t) + p1.y * t)
        # 如果当前像素的 y 值大于 buffer 中存储的 y 值（表示更靠近观察者）
        if buffer[x] < y:
            buffer[x] = y
            depth_color = int(y / 462 * 255)
            for h in range(0, 64):
                img.putpixel((x, h), color)
                y_img.putpixel((x, h), (depth_color, depth_color, depth_color))


if __name__ == '__main__':
    width = 800
    height = 64
    image = MyImage((width, height))
    y_image = MyImage((width, height))

    # line(20, 34, 744, 400, image, red)
    # line(120, 434, 444, 400, image, green)
    # line(330, 463, 594, 200, image, blue)

    # -sys.maxsize - 1 最小值
    y_buffer = [-sys.maxsize - 1] * width

    rasterize(Vec2([20, 34]), Vec2([744, 400]), image, y_image, red, y_buffer)
    rasterize(Vec2([120, 434]), Vec2([444, 400]), image, y_image, green, y_buffer)
    rasterize(Vec2([330, 463]), Vec2([594, 200]), image, y_image, blue, y_buffer)

    image.save('out.bmp')
    y_image.save('y_out.bmp')
