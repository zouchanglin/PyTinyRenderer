from PIL import Image

from vector import Vec3, Vec2


class OBJFile:
    def __init__(self, filename):
        self.model_file = filename
        self.vertex: list[Vec3] = []  # 顶点坐标数组
        self.tex_coord: list[Vec2] = []  # 纹理坐标数组
        self.norms: list[Vec3] = []  # 法向量数组

        self.facet_vrt: list[int] = []  # 面片顶点索引
        self.facet_tex: list[int] = []  # 面片纹理索引
        self.facet_nrm: list[int] = []  # 面片法向量索引

        self.diffuse_map: Image = None  # 漫反射贴图
        self.normal_map: Image = None  # 法线贴图
        self.specular_map: Image = None  # 镜面反射贴图

        self.parse()

    def parse(self):
        with open(self.model_file, 'r') as file:
            for line in file:
                components = line.strip().split()
                if not components:
                    continue
                if components[0] == 'v':
                    self.vertex.append(Vec3(*map(float, components[1:4])))
                elif components[0] == 'vn':
                    self.norms.append(Vec3(*map(float, components[1:4])))
                elif components[0] == 'vt':
                    self.tex_coord.append(Vec2(float(components[1]), 1 - float(components[2])))
                elif components[0] == 'f':
                    x = [[int(index.split('/')[0]), int(index.split('/')[1])] for index in components[1:]]
                    f, t, n = x[0][0], x[1][0], x[2][0]
                    self.facet_vrt.append(f - 1)
                    self.facet_tex.append(t - 1)
                    self.facet_nrm.append(n - 1)
        # 打印顶点、面片、纹理坐标和法向量的数量
        print(f"# v# {self.n_vertex()} f# {self.n_face()} vt# {len(self.tex_coord)} vn# {len(self.norms)}")

        # 加载纹理
        self.load_texture("_diffuse.tga", self.diffuse_map)
        # self.load_texture("_nm_tangent.tga", self.normal_map)
        # self.load_texture("_spec.tga", self.specular_map)

    def n_vertex(self) -> int:
        # 返回顶点数量
        return len(self.vertex)

    def n_face(self) -> int:
        # 返回面片数量
        return int(len(self.facet_vrt) / 3)

    def vert(self, i: int, n: int = None) -> Vec3:
        # 返回顶点坐标
        if n is None:
            return self.vertex[i]
        else:
            return self.vertex[self.facet_vrt[i * 3 + n]]

    def load_texture(self, suffix: str, img: Image):
        # 加载纹理
        dot = self.model_file.rfind('.')
        if dot == -1:
            return
        tex_file = self.model_file[:dot] + suffix
        img = Image.open(tex_file)
        print(f'Loading texture: {tex_file}--->{img}')
        # print(f"texture file {tex_file} loading {'ok' if img.load(tex_file) else 'failed'}")

    def normal(self, uvf: Vec2 = None, i: int = None, n: int = None) -> Vec3:
        """
        返回法向量
        """
        if uvf is not None:
            # 从法线贴图获取法线
            c = self.normal_map.getpixel((uvf.x * self.normal_map.width, uvf.y * self.normal_map.height))
            return Vec3(c[2], c[1], c[0]) * (2. / 255.) - Vec3(1, 1, 1)
        # 从法向量数组获取法线
        return self.norms[self.facet_nrm[i * 3 + n]]

    def uv(self, iface: int, n: int) -> Vec2:
        """
        返回纹理坐标
        """
        return self.tex_coord[self.facet_tex[iface * 3 + n]]
