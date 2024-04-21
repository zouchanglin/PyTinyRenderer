import math


class Vec2:
    def __init__(self, x, y=None):
        if isinstance(x, (list, tuple)) and len(x) == 2 and y is None:
            self.x, self.y = x[0], x[1]
        else:
            self.x, self.y = x, y

    @staticmethod
    def zero():
        return Vec3(0, 0)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):  # 向量和标量的乘法
            return Vec2(self.x * other, self.y * other)
        elif isinstance(other, Vec2):  # 两个向量的点积
            return self.x * other.x + self.y * other.y

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self, l=1):
        norm = self.norm()
        self.x *= l / norm
        self.y *= l / norm
        return self

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")

    def __str__(self):
        return f'({self.x}, {self.y})'


class Vec3:
    def __init__(self, x, y=None, z=None):
        if isinstance(x, (list, tuple)) and len(x) == 3 and y is None and z is None:
            self.x, self.y, self.z = x[0], x[1], x[2]
        else:
            self.x, self.y, self.z = x, y, z


    @staticmethod
    def zero():
        return Vec3(0, 0, 0)


    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, (int, float)):  # 向量和标量的乘法
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vec3):  # 两个向量的点积
            return self.x * other.x + self.y * other.y + self.z * other.z

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self, l=1):
        norm = self.norm()
        self.x *= l / norm
        self.y *= l / norm
        self.z *= l / norm
        return self

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Index out of range")

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'
