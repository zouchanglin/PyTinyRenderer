import random
from math import floor, ceil

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


# def triangle_old(p0: Vec2, p1: Vec2, p2: Vec2, img: MyImage):
#     if p0.y > p1.y:
#         p0, p1 = p1, p0
#     if p0.y > p2.y:
#         p0, p2 = p2, p0
#     if p1.y > p2.y:
#         p1, p2 = p2, p1
#     # line(p0.x, p0.y, p1.x, p1.y, img, green)
#     # line(p1.x, p1.y, p2.x, p2.y, img, green)
#     # line(p2.x, p2.y, p0.x, p0.y, img, red)
#     # 绘制下半部分
#     # 计算线段的斜率
#     slope0 = (p1.x - p0.x) / (p1.y - p0.y) if p1.y != p0.y else 0
#     slope1 = (p2.x - p0.x) / (p2.y - p0.y) if p2.y != p0.y else 0
#     # 从底部开始绘制
#     for y in range(int(p0.y), int(p1.y) + 1):
#         xs = p0.x + slope0 * (y - p0.y)  # 计算扫描线的起始点
#         xe = p0.x + slope1 * (y - p0.y)  # 计算扫描线的结束点
#         # 确保 xs < xe
#         if xs > xe:
#             xs, xe = xe, xs
#         # 绘制水平线
#         for x in range(int(xs), int(xe)):
#             img.putpixel((x, y), green)
#     # 绘制上半部分
#     slope2 = (p2.x - p1.x) / (p2.y - p1.y) if p2.y != p1.y else 0
#     for y in range(int(p1.y), int(p2.y)):
#         xs = p1.x + slope2 * (y - p1.y)  # 计算扫描线的起始点
#         xe = p0.x + slope1 * (y - p0.y)  # 计算扫描线的结束点
#
#         # 确保 xs < xe
#         if xs > xe:
#             xs, xe = xe, xs
#
#         # 绘制水平线
#         for x in range(int(xs), int(xe)):
#             img.putpixel((x, y), red)
#
#
# def triangle_old2(p0: Vec2, p1: Vec2, p2: Vec2, img: MyImage):
#     if p0.y > p1.y:
#         p0, p1 = p1, p0
#     if p0.y > p2.y:
#         p0, p2 = p2, p0
#     if p1.y > p2.y:
#         p1, p2 = p2, p1
#     # 计算线段的斜率
#     slope0 = (p1.x - p0.x) / (p1.y - p0.y) if p1.y != p0.y else 0
#     slope1 = (p2.x - p0.x) / (p2.y - p0.y) if p2.y != p0.y else 0
#     slope2 = (p2.x - p1.x) / (p2.y - p1.y) if p2.y != p1.y else 0
#
#     # 从底部开始绘制
#     for y in range(int(p0.y), int(p2.y)):
#         if y < p1.y:  # 如果在下半部分
#             xs = p0.x + slope0 * (y - p0.y)  # 计算扫描线的起始点
#         else:  # 如果在上半部分
#             xs = p1.x + slope2 * (y - p1.y)  # 计算扫描线的起始点
#         xe = p0.x + slope1 * (y - p0.y)  # 计算扫描线的结束点
#
#         # 确保 xs < xe
#         if xs > xe:
#             xs, xe = xe, xs
#
#         # 绘制水平线
#         for x in range(int(xs), int(xe)):
#             img.putpixel((x, y), green)
#
#
#
# def triangle_old3(p0: Vec2, p1: Vec2, p2: Vec2, img: MyImage):
#     # 如果点的纵坐标不是按升序排序的，则交换它们
#     if p0.y > p1.y:
#         p0, p1 = p1, p0
#     if p0.y > p2.y:
#         p0, p2 = p2, p0
#     if p1.y > p2.y:
#         p1, p2 = p2, p1
#
#     total_height = p2.y - p0.y
#     if total_height == 0:  # 如果三个点在同一水平线上，直接返回
#         return
#
#     for i in range(total_height):
#         second_half = i > p1.y - p0.y or p1.y == p0.y
#         segment_height = p2.y - p1.y if second_half else p1.y - p0.y
#         if segment_height == 0:  # 如果上半部分或下半部分的高度为0，跳过这一次循环
#             continue
#         alpha = i / total_height
#         beta = (i - (p1.y - p0.y if second_half else 0)) / segment_height
#         A = p0 + (p2 - p0) * alpha
#         B = p1 + (p2 - p1) * beta if second_half else p0 + (p1 - p0) * beta
#
#         # 确保 A.x < B.x
#         if A.x > B.x:
#             A, B = B, A
#
#         # 绘制水平线
#         for x in range(int(A.x), int(B.x)):
#             img.putpixel((x, p0.y + i), green)


def triangle_area_2d(a: Vec2, b: Vec2, c: Vec2) -> float:
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
    for P.y in range(min_y, max_y+1):
        for P.x in range(min_x, max_x+1):
            # 计算当前像素的重心坐标
            bc_screen = barycentric(p0, p1, p2, P)
            if bc_screen is None:
                continue
            # 如果像素的重心坐标的任何一个分量小于0，那么这个像素就在三角形的外部，我们就跳过它
            if bc_screen.x < 0 or bc_screen.y < 0 or bc_screen.z < 0:
                continue
            image.putpixel((P.x, P.y), color)


if __name__ == '__main__':
    width = 400
    height = 400
    image = MyImage((width, height))

    obj = OBJFile('african_head.obj')
    obj.parse()
    #
    # # 三角形三个顶点
    # t1 = [Vec2([10, 70]), Vec2([50, 160]), Vec2([70, 80])]
    # t2 = [Vec2([180, 50]), Vec2([150, 1]), Vec2([70, 180])]
    # t3 = [Vec2([180, 150]), Vec2([120, 160]), Vec2([130, 180])]
    # triangle(t1[0], t1[1], t1[2], image)
    # triangle(t2[0], t2[1], t2[2], image)
    # triangle(t3[0], t3[1], t3[2], image)

    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # for face in obj.faces:
    #     screen_coords = []
    #     for j in range(3):
    #         v: Vec3 = obj.vert(face[j])
    #         screen_coords.append(Vec2([int((v.x + 1) * width / 2), int((v.y + 1) * height / 2)]))
    #     triangle(screen_coords[0], screen_coords[1], screen_coords[2], image, random_color())
    # image.save('out.bmp')

    # light_dir = Vec3([0, 0, -1])
    # for face in obj.faces:
    #     screen_coords = []
    #     world_coords = [None, None, None]
    #     for j in range(3):
    #         v: Vec3 = obj.vert(face[j])
    #         screen_coords.append(Vec2([int((v.x + 1) * width / 2), int((v.y + 1) * height / 2)]))
    #         world_coords[j] = v
    #     # 计算三角形的法向量和光照强度
    #     n: Vec3 = (world_coords[2] - world_coords[0]).cross(world_coords[1] - world_coords[0])
    #     n.normalize()
    #     intensity = n * light_dir
    #     # 负的就剔除掉
    #     if intensity > 0:
    #         triangle(screen_coords[0], screen_coords[1], screen_coords[2], image,
    #                  (int(255 * intensity), int(255 * intensity), int(255 * intensity)))


    light_dir = Vec3([0, 0, -1])
    gamma = 2.2  # Gamma 值
    for face in obj.faces:
        screen_coords = []
        world_coords = [None, None, None]
        for j in range(3):
            v: Vec3 = obj.vert(face[j])
            screen_coords.append(Vec2([int((v.x + 1) * width / 2), int((v.y + 1) * height / 2)]))
            world_coords[j] = v
        # 计算三角形的法向量和光照强度
        n: Vec3 = (world_coords[2] - world_coords[0]).cross(world_coords[1] - world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # 负的就剔除掉
        if intensity > 0:
            # 进行 Gamma 矫正
            intensity = intensity ** (1 / gamma)
            triangle(screen_coords[0], screen_coords[1], screen_coords[2], image,
                     (int(255 * intensity), int(255 * intensity), int(255 * intensity)))

    image.save('out2.bmp')
