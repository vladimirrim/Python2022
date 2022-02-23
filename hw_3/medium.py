import numbers

import numpy as np


class StrMixin:

    def __str__(self):
        return '\n'.join([' '.join([str(e) for e in row]) for row in self.matrix])


class FileWriterMixin:

    def to_file(self, f):
        f.write(str(self))


class PropertyMixin:

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value


class Matrix(np.lib.mixins.NDArrayOperatorsMixin, StrMixin, FileWriterMixin, PropertyMixin):

    def __init__(self, m):
        self._matrix = np.asarray(m)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, Matrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.matrix if isinstance(x, Matrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


if __name__ == '__main__':
    np.random.seed(0)

    a = Matrix(np.random.randint(0, 10, (10, 10)))

    b = Matrix(np.random.randint(0, 10, (10, 10)))

    with open('artifacts/medium/matrix+.txt', "w") as f:
        (a + b).to_file(f)

    with open('artifacts/medium/matrix*.txt', "w") as f:
        (a * b).to_file(f)

    with open('artifacts/medium/matrix@.txt', "w") as f:
        (a @ b).to_file(f)
