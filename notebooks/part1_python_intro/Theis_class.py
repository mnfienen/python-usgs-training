import numpy as np
from scipy.special import exp1 as W


def set_time(t):
    if isinstance(t, (int, float, np.int, np.float)):
        t = np.array([t], dtype=np.float)
    elif isinstance(t, (list, tuple)):
        t = np.array(t, dtype=np.float)
    elif isinstance(t, (str)):
        print("dummy you can't use a string '{}'".format(t))
        return None
    return t


def Theis(r, t, Q=1.16, T=0.30, S=0.0008):
    t = set_time(t)
    u = np.zeros(t.shape[0], dtype=np.float)
    mask = t > 0.
    u[mask] = r ** 2 * S / (4 * T * t[mask])
    s = Q / (4 * np.pi * T) * W(u)
    return s


def Radius(ptw=(0., 0.), pto=(1000., 1000.)):
    return np.sqrt((ptw[0] - pto[0]) ** 2 +
                   (ptw[1] - pto[1]) ** 2)


def TheisArray(nrows, t, dx=100., ptw=(0, 0),
               Q=1.16, T=0.30, S=0.0008):
    t = set_time(t)
    ncols = nrows
    s = np.zeros((t.shape[0], nrows, ncols),
                 dtype=np.float)
    for i in range(nrows):
        for j in range(ncols):
            x = (j + 0.5) * dx
            y = (nrows - i - 0.5) * dx
            r = Radius(ptw, (x, y))
            s[:, i, j] = Theis(r, t, Q=Q, T=T, S=S)
    return s


if __name__ == "__main__":
    t = np.arange(0, 864000., 864.)
    print(t)
    s = Theis(Radius(), t)
    print(s)
    s = Theis(Radius(), [0., 100., 200.])
    print(s)
    sarray = TheisArray(10, [8.640000e10])
    print(sarray)
