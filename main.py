import sys

import numpy as np

from camera import Camera
# from gl import triangle
from gl import triangle_new
from image import MyImage
from matrix import Matrix
from obj import OBJFile
from shader import IShader
from vector import Vec3, Vec2

width = 900
height = 900
depth = 255

# 光照方向
light_dir = Vec3(0, 0, 1)

# 摄像机摆放的位置
eye = Vec3(1, 1, 3)
center = Vec3(0, 0, 0)
up = Vec3(0, 1, 0)

camera = Camera(eye, up, center - eye)


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
def projection_matrix():
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


model_ = model_matrix()
view_ = view_matrix(camera)
projection_ = projection_matrix()
viewport_ = viewport_matrix(width / 8, height / 8, width * 3 / 4, height * 3 / 4, depth)


class MyShader(IShader):
    def __init__(self):
        self.varying_intensity: Vec3 = Vec3(0, 0, 0)
        self.uv_coords: list[Vec2] = [Vec2.zero()] * 3

    def vertex(self, iface: int, n: int) -> Vec3:
        """
        顶点着色器
        :param iface: 面索引
        :param n: 顶点索引
        :return:
        """
        self.varying_intensity[n] = max(0, obj.normal(None, iface, n) * light_dir)
        self.uv_coords[j] = obj.uv(i, n)
        v: Vec3 = obj.vert(i, n)
        return homo_2_vertices(viewport_ * projection_division(projection_ * view_ * model_ * local_2_homo(v)))

    def fragment(self, bar: Vec3):
        """
        片元着色器
        :param bar: 重心坐标
        :return:
        """
        intensity = self.varying_intensity * bar
        if intensity < 0:
            return True, None

        uv0, uv1, uv2 = self.uv_coords
        uv = uv0 * bar.x + uv1 * bar.y + uv2 * bar.z
        tga = obj.diffuse_map
        color = tga.getpixel((int(uv.x * tga.width), tga.height - 1 - int(uv.y * tga.height)))
        color = (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))

        # color = (int(255 * intensity), int(255 * intensity), int(255 * intensity))
        return False, color


if __name__ == '__main__':
    shader: MyShader = MyShader()
    image = MyImage((width, height))
    z_image = MyImage((width, height))

    # -sys.maxsize - 1 最小值
    z_buffer = [-sys.maxsize - 1] * width * height

    obj = OBJFile('african_head.obj')

    for i in range(obj.n_face()):
        screen_coords = [None, None, None]  # 第i个面片三个顶点的屏幕坐标
        world_coords = [None, None, None]  # 第i个面片三个顶点的世界坐标
        uv_coords = [None, None, None]
        for j in range(3):
            screen_coords[j] = shader.vertex(i, j)
        triangle_new(screen_coords, shader, image, z_buffer)
    image.save('out.bmp')
