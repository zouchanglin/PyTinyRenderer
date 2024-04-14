from vector import Vec3


class OBJFile:
    def __init__(self, filename):
        self.filename = filename
        self.vertices = []
        self.texture_coords = []  # 添加一个新的列表来存储纹理坐标
        self.faces = []

    def parse(self):
        with open(self.filename, 'r') as file:
            for line in file:
                components = line.strip().split()
                if len(components) > 0:
                    if components[0] == 'v':
                        self.vertices.append([float(coord) for coord in components[1:]])
                    elif components[0] == 'vt':  # 添加一个新的条件来处理纹理坐标
                        self.texture_coords.append([float(coord) for coord in components[1:]])
                    elif components[0] == 'f':
                        # 修改这里，以便同时存储顶点和纹理坐标的索引
                        self.faces.append([[int(index.split('/')[0]),
                                            int(index.split('/')[1])] for index in components[1:]])
                        # self.faces.append([int(index.split('/')[0]) for index in components[1:]])

    def vert(self, i):
        """
        :param i: vertex index
        :param i: 因为obj文件的顶点索引是从1开始的，所以需要减1
        :return:
        """
        return Vec3(self.vertices[i - 1])

    def texcoord(self, i):  # 添加一个新的方法来获取纹理坐标
        """
        :param i: texture coordinate index
        :param i: 因为obj文件的纹理坐标索引是从1开始的，所以需要减1
        :return:
        """
        return Vec3(self.texture_coords[i - 1])
