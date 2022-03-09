import numpy as np

from hw_3.easy import Matrix

if __name__ == '__main__':
    a = Matrix([[1, 2],
                [3, 4]])

    b = Matrix([[33, -3],
                [3, 1]])

    c = Matrix([[4, 3],
                [2, 1]])

    d = b

    with open('artifacts/hard/A.txt', "w") as f:
        np.savetxt(f, a.matrix, '%d')

    with open('artifacts/hard/B.txt', "w") as f:
        np.savetxt(f, b.matrix, '%d')

    with open('artifacts/hard/C.txt', "w") as f:
        np.savetxt(f, c.matrix, '%d')

    with open('artifacts/hard/D.txt', "w") as f:
        np.savetxt(f, d.matrix, '%d')

    with open('artifacts/hard/AB.txt', "w") as f:
        np.savetxt(f, (a @ b).matrix, '%d')

    with open('artifacts/hard/CD.txt', "w") as f:
        np.savetxt(f, (c @ d).matrix, '%d')

    with open('artifacts/hard/hash.txt', "w") as f:
        f.write(f"AB: {hash(a @ b)},  CD: {hash(c @ d)}")

