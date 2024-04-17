import numpy as np


class Matrix:
    def __init__(self, nrows, ncols, init_value=0):
        self.nrows = nrows
        self.ncols = ncols
        self.data = np.full((nrows, ncols), init_value)

    def __getitem__(self, idx):
        return self.data[idx]

    def set_col(self, idx, v):
        self.data[:, idx] = v

    def col(self, idx):
        return self.data[:, idx]

    @staticmethod
    def identity(n):
        return Matrix(n, n, np.eye(n))

    def det(self):
        return np.linalg.det(self.data)

    def get_minor(self, row, col):
        minor = np.delete(self.data, row, axis=0)
        minor = np.delete(minor, col, axis=1)
        return Matrix(self.nrows - 1, self.ncols - 1, minor)

    def cofactor(self, row, col):
        return (-1) ** (row + col) * self.get_minor(row, col).det()

    def adjugate(self):
        adjugate = np.zeros((self.nrows, self.ncols))
        for i in range(self.nrows):
            for j in range(self.ncols):
                adjugate[i][j] = self.cofactor(i, j)
        return Matrix(self.nrows, self.ncols, adjugate)

    def invert_transpose(self):
        adjugate = self.adjugate()
        return adjugate / (adjugate[0] @ self.data[0])

    def invert(self):
        return self.invert_transpose().transpose()

    def transpose(self):
        return Matrix(self.ncols, self.nrows, np.transpose(self.data))

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.nrows, other.ncols, np.matmul(self.data, other.data))
        elif isinstance(other, (int, float)):
            return Matrix(self.nrows, self.ncols, self.data * other)
        else:
            raise ValueError("Unsupported operand type for *: 'Matrix' and '{}'".format(type(other)))

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Matrix(self.nrows, self.ncols, self.data / other)
        else:
            raise ValueError("Unsupported operand type for /: 'Matrix' and '{}'".format(type(other)))

    def __add__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.nrows, self.ncols, np.add(self.data, other.data))
        else:
            raise ValueError("Unsupported operand type for +: 'Matrix' and '{}'".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.nrows, self.ncols, np.subtract(self.data, other.data))
        else:
            raise ValueError("Unsupported operand type for -: 'Matrix' and '{}'".format(type(other)))

    @staticmethod
    def from_np(np_matrix):
        m = Matrix(np_matrix.shape[0], np_matrix.shape[1])
        m.m = np_matrix
        return m

    def __str__(self):
        return str(self.data)
