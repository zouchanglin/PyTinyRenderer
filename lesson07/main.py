import sys

from camera import Camera
from color import Color
from gl import triangle, get_mvp, projection_division, homo_2_vertices, local_2_homo
from image import MyImage
from matrix import Matrix
from obj import OBJFile
from shader import IShader
from vector import Vec3, Vec2

width = 1200
height = 1200
depth = 255

# 光照方向
light_dir = Vec3(0, 0, 1)

# 摄像机摆放的位置
eye = Vec3(1, 1, 3)
center = Vec3(0, 0, 0)
up = Vec3(0, 1, 0)

camera = Camera(eye, up, center - eye)


model_, view_, projection_, viewport_ = get_mvp(camera, eye, width, height, depth)


class MyShader(IShader):
    def __init__(self):
        # self.varying_intensity: Vec3 = Vec3(0, 0, 0)
        # self.uv_coords: list[Vec2] = [Vec2.zero()] * 3
        self.varying_uv: Matrix = Matrix(2, 3)
        self.uniform_M: Matrix = Matrix.identity(4)
        self.uniform_MIT: Matrix = Matrix.identity(4)

    def vertex(self, iface: int, n: int) -> Vec3:
        """
        顶点着色器
        :param iface: 面索引
        :param n: 顶点索引
        :return:
        """
        # self.varying_intensity[n] = max(0, obj.normal(None, iface, n) * light_dir)
        # self.uv_coords[j] = obj.uv(i, n)
        # v: Vec3 = obj.vert(i, n)
        # return homo_2_vertices(viewport_ * projection_division(projection_ * view_ * model_ * local_2_homo(v)))

        # 基于法线贴图渲染
        self.varying_uv.set_col(n, obj.uv(iface, n))
        v: Vec3 = obj.vert(iface, n)
        return homo_2_vertices(viewport_ * projection_division(projection_ * view_ * model_ * local_2_homo(v)))


    def fragment(self, bar: Vec3):
        """
        片元着色器
        :param bar: 重心坐标
        :return:
        """
        # intensity = self.varying_intensity * bar
        # if intensity < 0:
        #     return True, None
        # uv0, uv1, uv2 = self.uv_coords
        # uv = uv0 * bar.x + uv1 * bar.y + uv2 * bar.z
        # tga = obj.diffuse_map
        # color = tga.getpixel((int(uv.x * tga.width), tga.height - 1 - int(uv.y * tga.height)))
        # color = Color(int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))
        # return False, color

        uv: Vec2 = Vec2((self.varying_uv.m @ bar.to_matrix())[0][0], (self.varying_uv.m @ bar.to_matrix())[1][0])

        n = (self.uniform_MIT * local_2_homo(obj.normal(uv))).m
        n: Vec3 = Vec3(n[0][0], n[1][0], n[2][0]).normalize()
        l = (self.uniform_M * local_2_homo(light_dir)).m
        l: Vec3 = Vec3(l[0][0], l[1][0], l[2][0]).normalize()

        r = (n*(n*l*2.) - l).normalize()
        specular = pow(max(r.z, 0.0), obj.specular(uv))

        intensity: float = max(0.0, n * l)
        if intensity < 0:
            return True, None
        tga = obj.diffuse_map
        color = tga.getpixel((int(uv.x * tga.width), tga.height - 1 - int(uv.y * tga.height)))
        # color = [255, 255, 255]
        a = int(color[0] * (intensity + 0.8 * specular))
        b = int(color[1] * (intensity + 0.8 * specular))
        c = int(color[2] * (intensity + 0.8 * specular))
        color = (min(a, 255), min(b, 255), min(c, 255))
        return False, color


if __name__ == '__main__':
    shader: MyShader = MyShader()
    shader.uniform_M = projection_ * model_ * view_
    shader.uniform_MIT = (projection_ * model_ * view_).transpose()

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
        triangle(screen_coords, shader, image, z_buffer)
    image.save('out.bmp')