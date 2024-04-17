import sys

import numpy as np
from PIL import Image

from camera import Camera
from gl import lookat, viewport, projection, triangle
from image import MyImage
from lesson04.main import model_matrix, projection_matrix, viewport_matrix, local_2_homo, \
    projection_division
from matrix import Matrix
from obj import OBJFile
from shader import IShader
from vector import Vec3, Vec4

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

width = 600
height = 600

light_dir = Vec3(0, 0, 1)
eye = Vec3(1, 1, 2)
center = Vec3(0, 0, 0)
up = Vec3(0, 1, 0)


def view_matrix(camera: Camera):
    r_inverse = np.identity(4)
    t_inverse = np.identity(4)
    for i in range(3):
        r_inverse[0][i] = camera.right.get(i)
        r_inverse[1][i] = camera.up.get(i)
        r_inverse[2][i] = -camera.front.get(i)

        t_inverse[i][3] = -camera.position.get(i)
    view = np.dot(r_inverse, t_inverse)
    return Matrix.from_np(view)


def homo_2_vertices(m: Matrix):
    """
    去掉第四个分量，将其恢复到三维坐标
    """
    return Vec3(int(m[0][0]), int(m[1][0]), int(m[2][0]))


if __name__ == '__main__':
    obj: OBJFile = OBJFile('african_head.obj')

    lookat(eye, center, up)
    viewport(width / 8, height / 8, width * 3 / 4, height * 3 / 4)
    projection(-1. / (eye - center).norm())
    light_dir.normalize()

    image = MyImage((width, height))
    z_image = MyImage((width, height))
    # -sys.maxsize - 1 最小值
    z_buffer = [-sys.maxsize - 1] * width * height

    eye_position = Vec3(1, 1, 3)
    center = Vec3(0, 0, 0)
    camera = Camera(eye_position, Vec3(0, 1, 0), center - eye_position)
    model_ = model_matrix()
    view_ = view_matrix(camera)
    projection_ = projection_matrix()
    viewport_ = viewport_matrix(width / 8, height / 8, width * 3 / 4, height * 3 / 4, 255)

    class MyShader(IShader):
        def __init__(self):
            self.varying_intensity: Vec3 = Vec3(0, 0, 0)

        def vertex(self, iface: int, n: int) -> Vec4:
            self.varying_intensity[n] = max(0, obj.normal(None, iface, n) * light_dir)

            # def embed(n1, v, fill=1):
            #     ret = [0] * n1
            #     n2 = len(v)
            #     for i in range(n1):
            #         ret[i] = v[i] if i < n2 else fill
            #     return ret
            #
            # x = embed(4, [obj.vert(iface, n).x, obj.vert(iface, n).y, obj.vert(iface, n).z])
            # gl_vertex = Vec4(x[0], x[1], x[2], x[3])
            # from gl import Viewport, Projection, ModelView
            # ret = Viewport.data @ Projection.data @ ModelView.data @ np.array([gl_vertex.x, gl_vertex.y, gl_vertex.z, gl_vertex.w])
            #
            # return Vec4(ret[0], ret[1], ret[2], ret[3])

            return homo_2_vertices(viewport_ * projection_division(
                projection_ * view_ * model_ * local_2_homo(obj.vert(iface, n))))

        def fragment(self, bar: Vec3):
            intensity = self.varying_intensity * bar
            color = (255 * intensity, 255 * intensity, 255 * intensity)
            return color


    shader = MyShader()

    for i in range(obj.n_face()):
        screen_coords: list[Vec4] = [None, None, None]
        for j in range(3):
            screen_coords[j] = shader.vertex(i, j)
        triangle(screen_coords, shader, image, z_buffer)
    image.save('out.bmp')
    z_image.save('z_out.bmp')
