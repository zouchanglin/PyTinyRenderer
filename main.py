import sys
from PIL import Image
from image import MyImage
from matrix import Matrix
from obj import OBJFile
from vector import Vec3, Vec2

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


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


def triangle(p0: Vec3, p1: Vec3, p2: Vec3,
             uv0: Vec2, uv1: Vec2, uv2: Vec2,
             intensity, img: MyImage, tga: Image):
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

            # 使用重心坐标来插值纹理坐标
            uv = uv0 * bc_screen.x + uv1 * bc_screen.y + uv2 * bc_screen.z
            # 使用插值后的纹理坐标来从TGA文件中获取颜色
            # 此TGA文件是从左上角开始的，所以需要将纵坐标反转
            color = tga.getpixel((int(uv.x * tga.width), tga.height - 1 - int(uv.y * tga.height)))
            color = (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))

            # 计算当前像素的深度
            z = p0.z * bc_screen.x + p1.z * bc_screen.y + p2.z * bc_screen.z

            # 检查Z缓冲区，如果当前像素的深度比Z缓冲区中的值更近，那么就更新Z缓冲区的值，并绘制像素
            idx = P.x + P.y * img.width
            if z_buffer[idx] < z:
                z_buffer[idx] = z
                image.putpixel((P.x, P.y), color)


# 摄像机摆放的位置
cameraPos = Vec3([0, 0, 3])


def local_2_homo(v: Vec3):
    """
    局部坐标变换成齐次坐标
    """
    m = Matrix(4, 1)
    m[0][0] = v.x
    m[1][0] = v.y
    m[2][0] = v.z
    m[3][0] = 1.0
    return m


# 模型变换矩阵
def model_matrix():
    return Matrix.identity(4)


# 视图变换矩阵
def view_matrix():
    return Matrix.identity(4)


# 透视投影变换矩阵
def projection_matrix():
    projection = Matrix.identity(4)
    projection[3][2] = -1.0 / cameraPos.z
    return projection


# 透视除法
def projection_division(m: Matrix):
    m[0][0] = m[0][0] / m[3][0]
    m[1][0] = m[1][0] / m[3][0]
    m[2][0] = m[2][0] / m[3][0]
    m[3][0] = 1.0
    return m


def viewport_matrix(x, y, w, h, depth):
    m = Matrix.identity(4)
    m[0][3] = x + w / 2.
    m[1][3] = y + h / 2.
    m[2][3] = depth / 2.

    m[0][0] = w / 2.
    m[1][1] = h / 2.
    m[2][2] = depth / 2.
    return m


def homo_2_vertices(m: Matrix):
    return Vec3([int(m[0][0]), int(m[1][0]), int(m[2][0])])


if __name__ == '__main__':
    width = 600
    height = 600
    depth = 255

    tga: Image = Image.open('african_head_diffuse.tga')

    image = MyImage((width, height))

    # -sys.maxsize - 1 最小值
    z_buffer = [-sys.maxsize - 1] * width * height

    obj = OBJFile('african_head.obj')
    obj.parse()

    model_ = model_matrix()
    view_ = view_matrix()
    projection_ = projection_matrix()
    viewport_ = viewport_matrix(width / 8, height / 8, width * 3 / 4, height * 3 / 4, depth)

    light_dir = Vec3([0, 0, -1])
    gamma = 2.2
    for face in obj.faces:
        screen_coords = [None, None, None]
        world_coords = [None, None, None]
        uv_coords = [None, None, None]
        for j in range(3):
            v: Vec3 = obj.vert(face[j][0])
            # screen_coords.append(Vec3([int((v.x + 1) * width / 2), int((v.y + 1) * height / 2), v.z]))
            # screen_coords.append(Vec3([int((v.x + 1) * width / 2), int((v.y + 1) * height / 2), v.z]))

            world_coords[j] = v
            uv_coords[j] = obj.texcoord(face[j][1])  # 获取纹理坐标

            screen_coords[j] = homo_2_vertices(viewport_ *
                                               projection_division(projection_ * view_ * model_ * local_2_homo(v)))

        # 计算三角形的法向量和光照强度
        n: Vec3 = (world_coords[2] - world_coords[0]).cross(world_coords[1] - world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # 负的就剔除掉
        if intensity > 0:
            intensity = intensity ** (1 / gamma)
            triangle(screen_coords[0], screen_coords[1], screen_coords[2],
                     uv_coords[0], uv_coords[1], uv_coords[2],
                     intensity, image, tga)

    image.save('out.bmp')
