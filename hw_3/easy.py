import numpy as np


class MatrixHashMixin:

    def __hash__(self):
        """ Trace of the matrix"""

        return sum([self.matrix[i][i] for i in range(min(self.shape))])


class Matrix(MatrixHashMixin):
    def __init__(self, m):
        if len(m) == 0:
            raise ValueError(f"Invalid shape of the matrix")
        self.shape = (len(m), len(m[0]))

        for row in m:
            if len(row) != self.shape[1]:
                raise ValueError(f"Invalid lengths of the rows: {len(row)} and {self.shape[1]}")

        self._matrix = [[m[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError(f"Incompatible shapes: Mat1 is {self.shape} and Mat2 is {other.shape}")

        return Matrix([[self._matrix[i][j] + other.matrix[i][j] for j in range(self.shape[1])]
                       for i in range(self.shape[0])])

    def __mul__(self, other):
        if self.shape != other.shape:
            raise ValueError(f"Incompatible shapes: Mat1 is {self.shape} and Mat2 is {other.shape}")

        return Matrix([[self._matrix[i][j] * other.matrix[i][j] for j in range(self.shape[1])]
                       for i in range(self.shape[0])])

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"Incompatible shapes for multiplication: Mat1 is {self.shape} and Mat2 is {other.shape}")

        return Matrix([[sum([self._matrix[i][k] * other.matrix[k][j] for k in range(self.shape[1])])
                        for j in range(other.shape[1])] for i in range(self.shape[0])])

    @property
    def matrix(self):
        return self._matrix


if __name__ == '__main__':
    np.random.seed(0)

    a = Matrix(np.random.randint(0, 10, (10, 10)))

    b = Matrix(np.random.randint(0, 10, (10, 10)))

    with open('artifacts/easy/matrix+.txt', "w") as f:
        np.savetxt(f, (a + b).matrix, '%d')

    with open('artifacts/easy/matrix*.txt', "w") as f:
        np.savetxt(f, (a * b).matrix, '%d')

    with open('artifacts/easy/matrix@.txt', "w") as f:
        np.savetxt(f, (a @ b).matrix, '%d')

