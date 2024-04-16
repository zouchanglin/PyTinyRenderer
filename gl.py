import numpy as np

from matrix import Matrix
from shader import IShader
from vector import Vec3, Vec2, Vec4

ModelView: Matrix
Viewport: Matrix
Projection: Matrix


def viewport(x, y, w, h, depth=255):
    global Viewport
    m = Matrix.identity(4)
    m[0][3] = x + w / 2.0
    m[1][3] = y + h / 2.0
    m[2][3] = depth / 2.0

    m[0][0] = w / 2.0
    m[1][1] = h / 2.0
    m[2][2] = depth / 2.0
    Viewport = m


def projection(f=0):
    global Projection
    proj = Matrix.identity(4)
    proj[3][2] = -1.0 / f
    Projection = proj


def lookat(eye, center, up):
    global ModelView
    z = (eye - center).normalize()
    x = up.cross(z).normalize()
    y = z.cross(x).normalize()
    Minv = Matrix.identity(4)
    Tr = Matrix.identity(4)
    for i in range(3):
        Minv[0][i] = x[i]
        Minv[1][i] = y[i]
        Minv[2][i] = z[i]
        Tr[i][3] = -center[i]
    ModelView = Minv * Tr


def triangle_area_2d(a: Vec2, b: Vec2, c: Vec2) -> float:
    """
    计算三角形面积
    """
    return .5 * ((b.y - a.y) * (b.x + a.x) + (c.y - b.y) * (c.x + b.x) + (a.y - c.y) * (a.x + c.x))


def barycentric(tri, p):
    a, b, c = tri
    total_area = triangle_area_2d(a, b, c)
    if total_area == 0:
        return None
    u = triangle_area_2d(p, b, c) / total_area
    v = triangle_area_2d(p, c, a) / total_area
    w = triangle_area_2d(p, a, b) / total_area
    return Vec3([u, v, w])


def triangle(v: list[Vec4], shader: IShader, image, z_buffer):
    for x in v:
        pass
    # 转换到屏幕坐标
    screen_coords = [Viewport.m * x for x in v]

    # 计算包围盒
    min_x = max(0, min([v.x for v in screen_coords]))
    max_x = min(image.width - 1, max([v.x for v in screen_coords]))
    min_y = max(0, min([v.y for v in screen_coords]))
    max_y = min(image.height - 1, max([v.y for v in screen_coords]))

    # 对包围盒中的每个像素进行插值
    P = Vec2((0, 0))
    for P.y in range(min_y, max_y + 1):
        for P.x in range(min_x, max_x + 1):
            bc_screen = barycentric(screen_coords, P)
            if bc_screen is None or bc_screen.x < 0 or bc_screen.y < 0 or bc_screen.z < 0:
                continue
            bc_clip = np.array([bc_screen.get(i) / v[i].w for i in range(3)])
            bc_clip /= bc_clip.sum()
            frag_depth = np.dot(bc_clip, [v[i].z for i in range(3)])
            idx = int(P.x + P.y * image.width)
            if frag_depth > z_buffer[idx]:
                continue

            # 插值Z值
            z = sum([v.z * bc_screen.get(i) for i, v in enumerate(screen_coords)])

            # 检查Z-buffer，如果当前像素的深度比Z-buffer中的值更近，那么就更新Z-buffer的值，并绘制像素
            idx = int(P.x + P.y * image.width)
            if z_buffer[idx] < z:
                z_buffer[idx] = z
                color = shader.fragment(bc_screen)
                image.putpixel((int(P.x), int(P.y)), color)

