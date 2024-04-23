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
                    self.tex_coord.append(Vec2(float(components[1]), float(components[2])))
                    # self.tex_coord.append(float(coord) for coord in components[1:])
                elif components[0] == 'f':
                    for sp in components[1:]:
                        p = sp.split('/')
                        self.facet_vrt.append(int(p[0])-1)
                        self.facet_tex.append(int(p[1])-1)
                        self.facet_nrm.append(int(p[2])-1)
        # 打印顶点、面片、纹理坐标和法向量的数量
        print(f"# v# {self.n_vertex()} f# {self.n_face()} vt# {len(self.tex_coord)} vn# {len(self.norms)}")

        # 加载纹理
        self.load_texture("_diffuse.tga", self.diffuse_map)
        self.load_texture("_nm_tangent.tga", self.normal_map)
        self.load_texture("_spec.tga", self.specular_map)

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
        # 判断文件是否存在
        if suffix.endswith('_diffuse.tga'):
            self.diffuse_map = Image.open(tex_file)
            print(f'Loading _diffuse_map texture: {tex_file}--->{img}')
        elif suffix.endswith('_nm_tangent.tga'):
            self.normal_map = Image.open(tex_file)
            print(f'Loading _nm_tangent texture: {tex_file}')
        elif suffix.endswith('_spec.tga'):
            self.specular_map = Image.open(tex_file)
            print(f'Loading _spec texture: {tex_file}')

    def normal(self, uvf: Vec2 = None, i: int = None, n: int = None) -> Vec3:
        """
        返回法向量
        """
        if uvf is not None:
            # 从法线贴图获取法线
            c = self.normal_map.getpixel((uvf.x * self.normal_map.width, self.normal_map.height - 1 - uvf.y * self.normal_map.height))
            return Vec3(c[2], c[1], c[0]) * (2. / 255.) - Vec3(1, 1, 1)
        # 从法向量数组获取法线
        return self.norms[self.facet_nrm[i * 3 + n]]

    def specular(self, uvf: Vec2 = None):
        c = self.specular_map.getpixel((uvf.x * self.specular_map.width, self.specular_map.height - 1 - uvf.y * self.specular_map.height))
        return c / 128

    def uv(self, iface: int, n: int) -> Vec2:
        """
        返回纹理坐标
        """
        return self.tex_coord[self.facet_tex[iface * 3 + n]]
