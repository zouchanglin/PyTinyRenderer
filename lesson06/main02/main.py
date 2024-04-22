import sys

from camera import Camera
from color import Color
from gl import triangle, get_mvp, projection_division, homo_2_vertices, local_2_homo
from image import MyImage
from obj import OBJFile
from shader import IShader
from vector import Vec3, Vec2

width = 900
height = 900
depth = 255

# 光照方向
light_dir = Vec3(0, 0, 1)

# 摄像机摆放的位置
eye = Vec3(1, 1, 2)
center = Vec3(0, 0, 0)
up = Vec3(0, 1, 0)

camera = Camera(eye, up, center - eye)


model_, view_, projection_, viewport_ = get_mvp(camera, eye, width, height, depth)


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

        if intensity > .85:
            intensity = 1
        elif intensity > .60:
            intensity = .80
        elif intensity > .45:
            intensity = .60
        elif intensity > .30:
            intensity = .45
        elif intensity > .15:
            intensity = .30
        else:
            intensity = 0
        color = Color(int(255 * intensity), int(155 * intensity), 0)
        # uv0, uv1, uv2 = self.uv_coords
        # uv = uv0 * bar.x + uv1 * bar.y + uv2 * bar.z
        # tga = obj.diffuse_map
        # color = tga.getpixel((int(uv.x * tga.width), tga.height - 1 - int(uv.y * tga.height)))
        # color = Color(int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))
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
        triangle(screen_coords, shader, image, z_buffer)
    image.save('out.bmp')

    # z_image = MyImage((width, height))
    # # 在所有三角形都被渲染后，遍历Z-buffer以找到最大和最小的深度值
    # z_min = min(z for z in z_buffer if z != -sys.maxsize - 1)
    # z_max = max(z for z in z_buffer if z != -sys.maxsize - 1)
    #
    # # 然后，遍历Z-buffer，对每个深度值进行归一化，然后将其映射到0到255的范围
    # for i in range(len(z_buffer)):
    #     if z_buffer[i] != -sys.maxsize - 1:
    #         # 首先将Z值偏移，使其变为正数
    #         z_positive = z_buffer[i] - z_min
    #         # 然后归一化深度值
    #         z_normalized = z_positive / (z_max - z_min)
    #         # 映射到0到255的范围
    #         depth_color = int(z_normalized * 255)
    #         # 在深度图中设置像素颜色
    #         x = i % width
    #         y = i // width
    #         z_image.putpixel((x, y), (depth_color, depth_color, depth_color))
    #
    # z_image.save('z_out.bmp')
