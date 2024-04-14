from vector import Vec3


class OBJFile:
    def __init__(self, filename):
        self.filename = filename
        self.vertices = []
        self.faces = []

    def parse(self):
        with open(self.filename, 'r') as file:
            for line in file:
                components = line.strip().split()
                if len(components) > 0:
                    if components[0] == 'v':
                        self.vertices.append([float(coord) for coord in components[1:]])
                    elif components[0] == 'f':
                        self.faces.append([int(index.split('/')[0]) for index in components[1:]])

    def vert(self, i):
        """
        :param i: vertex index
        :param i: 因为obj文件的顶点索引是从1开始的，所以需要减1
        :return:
        """
        return Vec3(self.vertices[i - 1])
