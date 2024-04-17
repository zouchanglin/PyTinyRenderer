import math


class Vec2:
    def __init__(self, x, y):
        self.x, self.y = x, y

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

    def get(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y

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
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

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

    def get(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z

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


class Vec4:
    def __init__(self, x, y, z, w):
        self.x, self.y, self.z, self.w = x, y, z, w

    def __add__(self, other):
        return Vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __mul__(self, other):
        if isinstance(other, (int, float)):  # 向量和标量的乘法
            return Vec4(self.x * other, self.y * other, self.z * other, self.w * other)
        elif isinstance(other, Vec4):  # 两个向量的点积
            return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def normalize(self, l=1):
        norm = self.norm()
        self.x *= l / norm
        self.y *= l / norm
        self.z *= l / norm
        self.w *= l / norm
        return self

    def get(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        elif i == 3:
            return self.w

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        elif index == 3:
            return self.w
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        elif index == 3:
            self.w = value
        else:
            raise IndexError("Index out of range")

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z}, {self.w})'
