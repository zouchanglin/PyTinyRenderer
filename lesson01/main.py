from obj import OBJFile
from vector import Vec3
from image import MyImage


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


if __name__ == '__main__':
    width = 800
    height = 800
    image = MyImage((width, height))
    white = (255, 255, 255)
    obj = OBJFile('african_head.obj')
    obj.parse()

    for face in obj.faces:
        for j in range(3):
            v0: Vec3 = obj.vert(face[j])
            v1: Vec3 = obj.vert(face[(j + 1) % 3])
            x0 = int((v0.x + 1) * width / 2)
            y0 = int((v0.y + 1) * height / 2)
            x1 = int((v1.x + 1) * width / 2)
            y1 = int((v1.y + 1) * height / 2)
            line(x0, y0, x1, y1, image, white)
    image.save('out.bmp')
