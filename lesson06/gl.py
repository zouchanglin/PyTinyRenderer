import numpy as np

from camera import Camera
from image import MyImage
from matrix import Matrix
from shader import IShader
from vector import Vec3, Vec2


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


def view_matrix(camera: Camera):
    r_inverse = np.identity(4)
    t_inverse = np.identity(4)
    for i in range(3):
        r_inverse[0][i] = camera.right[i]
        r_inverse[1][i] = camera.up[i]
        r_inverse[2][i] = -camera.front[i]

        t_inverse[i][3] = -camera.position[i]
    view = np.dot(r_inverse, t_inverse)
    return Matrix.from_np(view)


# 透视投影变换矩阵（调整FOV）
def projection_matrix(eye):
    projection = Matrix.identity(4)
    projection[3][2] = -1.0 / eye.z * 0.01
    return projection


# 此时我们的所有的顶点已经经过了透视投影变换，接下来需要进行透视除法
def projection_division(m: Matrix):
    m[0][0] = m[0][0] / m[3][0]
    m[1][0] = m[1][0] / m[3][0]
    m[2][0] = m[2][0] / m[3][0]
    m[3][0] = 1.0
    return m


def viewport_matrix(x, y, w, h, depth):
    """
    视口变换将NDC坐标转换为屏幕坐标
    """
    m = Matrix.identity(4)
    m[0][3] = x + w / 2.
    m[1][3] = y + h / 2.
    m[2][3] = depth / 2.

    m[0][0] = w / 2.
    m[1][1] = h / 2.
    m[2][2] = depth / 2.
    return m


def homo_2_vertices(m: Matrix):
    """
    去掉第四个分量，将其恢复到三维坐标
    """
    return Vec3([int(m[0][0]), int(m[1][0]), int(m[2][0])])


def get_mvp(camera, eye, width, height, depth):
    model_ = model_matrix()
    view_ = view_matrix(camera)
    projection_ = projection_matrix(eye)
    viewport_ = viewport_matrix(width / 8, height / 8, width * 3 / 4, height * 3 / 4, depth)
    return model_, view_, projection_, viewport_


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
    return Vec3(u, v, w)


def triangle(screen_coords: list[Vec3], shader: IShader, img: MyImage, z_buffer):
    p0, p1, p2 = screen_coords
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
            skip, color = shader.fragment(bc_screen)
            if skip:
                continue
            # 计算当前像素的深度
            z = p0.z * bc_screen.x + p1.z * bc_screen.y + p2.z * bc_screen.z
            # 检查Z缓冲区，如果当前像素的深度比Z缓冲区中的值更近，那么就更新Z缓冲区的值，并绘制像素
            idx = P.x + P.y * img.width
            if z_buffer[idx] < z:
                z_buffer[idx] = z
                img.putpixel((P.x, P.y), color)
