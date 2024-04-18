import sys

import numpy as np
from PIL import Image

from camera import Camera
from gl import triangle
from image import MyImage
from matrix import Matrix
from obj import OBJFile
from vector import Vec3, Vec2


# 摄像机摆放的位置
eye_position = Vec3(1, 1, 3)
center = Vec3(0, 0, 0)

camera = Camera(eye_position, Vec3(0, 1, 0), center - eye_position)


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


# 透视投影变换矩阵
def projection_matrix():
    projection = Matrix.identity(4)
    projection[3][2] = -1.0 / eye_position.z
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


if __name__ == '__main__':
    width = 900
    height = 900
    depth = 255

    tga: Image = Image.open('african_head_diffuse.tga')

    image = MyImage((width, height))
    z_image = MyImage((width, height))

    # -sys.maxsize - 1 最小值
    z_buffer = [-sys.maxsize - 1] * width * height

    obj = OBJFile('african_head.obj')
    obj.parse()

    model_ = model_matrix()
    view_ = view_matrix(camera)
    projection_ = projection_matrix()
    viewport_ = viewport_matrix(width / 8, height / 8, width * 3 / 4, height * 3 / 4, depth)

    light_dir = Vec3([0, 0, -1])
    gamma = 2.2
    for i in range(obj.n_face()):
        screen_coords = [None, None, None]  # 第i个面片三个顶点的屏幕坐标
        world_coords = [None, None, None]  # 第i个面片三个顶点的世界坐标
        uv_coords = [None, None, None]
        for j in range(3):
            v: Vec3 = obj.vert(i, j)
            world_coords[j] = v
            uv_coords[j] = obj.uv(i, j)  # 获取纹理坐标

            screen_coords[j] = homo_2_vertices(viewport_ * projection_division(
                projection_ * view_ * model_ * local_2_homo(v)))

        # 计算三角形的法向量和光照强度
        n: Vec3 = (world_coords[2] - world_coords[0]).cross(world_coords[1] - world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # 负的就剔除掉
        if intensity > 0:
            intensity = intensity ** (1 / gamma)
            triangle(screen_coords[0], screen_coords[1], screen_coords[2],
                     uv_coords[0], uv_coords[1], uv_coords[2],
                     intensity, image, tga, z_buffer)

    image.save('out.bmp')

    # 最后绘制深度图z_img
    # 然后，遍历Z-buffer，对每个深度值进行归一化，然后将其映射到0到255的范围
    # 在所有三角形都被渲染后，遍历Z-buffer以找到最大和最小的深度值
    z_min = min(z for z in z_buffer if z != -sys.maxsize - 1)
    z_max = max(z for z in z_buffer if z != -sys.maxsize - 1)

    # 然后，遍历Z-buffer，对每个深度值进行归一化，然后将其映射到0到255的范围
    for i in range(len(z_buffer)):
        if z_buffer[i] != -sys.maxsize - 1:
            # 首先将Z值偏移，使其变为正数
            z_positive = z_buffer[i] - z_min
            # 然后归一化深度值
            z_normalized = z_positive / (z_max - z_min)
            # 映射到0到255的范围
            depth_color = int(z_normalized * 255)
            # 在深度图中设置像素颜色
            x = i % width
            y = i // width
            z_image.putpixel((x, y), (depth_color, depth_color, depth_color))

    z_image.save('z_out.bmp')
