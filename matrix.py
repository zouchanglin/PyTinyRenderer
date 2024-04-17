import numpy as np


class Matrix:
    def __init__(self, r=4, c=4):
        self.m = np.zeros((r, c), dtype=float)
        self.rows = r
        self.cols = c

    @staticmethod
    def identity(dimensions):
        mat = Matrix(dimensions, dimensions)
        mat.m = np.eye(dimensions, dtype=float)
        return mat

    def __getitem__(self, i):
        assert 0 <= i < self.rows
        return self.m[i]

    def __mul__(self, a):
        assert self.cols == a.rows
        return Matrix.from_np(self.m @ a.m)

    def transpose(self):
        return Matrix.from_np(np.transpose(self.m))

    def inverse(self):
        assert self.rows == self.cols
        return Matrix.from_np(np.linalg.inv(self.m))

    @staticmethod
    def from_np(np_matrix):
        m = Matrix(np_matrix.shape[0], np_matrix.shape[1])
        m.m = np_matrix
        return m

    def __str__(self):
        return str(self.m)
