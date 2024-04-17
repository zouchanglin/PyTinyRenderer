import sys

import numpy as np

from gl import lookat, viewport, projection, triangle
from image import MyImage
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


if __name__ == '__main__':
    obj: OBJFile = OBJFile('../african_head.obj')

    lookat(eye, center, up)
    viewport(width / 8, height / 8, width * 3 / 4, height * 3 / 4)
    projection(-1. / (eye - center).norm())
    light_dir.normalize()

    image = MyImage((width, height))
    z_image = MyImage((width, height))
    # -sys.maxsize - 1 最小值
    z_buffer = [-sys.maxsize - 1] * width * height


    class MyShader(IShader):
        def __init__(self):
            self.varying_intensity: Vec3 = Vec3(0, 0, 0)

        def vertex(self, iface: int, n: int) -> Vec4:
            self.varying_intensity[n] = max(0, obj.normal(None, iface, n) * light_dir)

            def embed(n1, v, fill=1):
                ret = [0] * n1
                n2 = len(v)
                for i in range(n1):
                    ret[i] = v[i] if i < n2 else fill
                return ret

            x = embed(4, [obj.vert(iface, n).x, obj.vert(iface, n).y, obj.vert(iface, n).z])
            gl_vertex = Vec4(x[0], x[1], x[2], x[3])
            from gl import Viewport, Projection, ModelView
            ret = Viewport.data @ Projection.data @ ModelView.data @ np.array([gl_vertex.x, gl_vertex.y, gl_vertex.z, gl_vertex.w])

            return Vec4(ret[0], ret[1], ret[2], ret[3])

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
