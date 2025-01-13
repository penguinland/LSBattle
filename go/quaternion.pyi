"""
# cython: profile=False
cimport cython
from libc.math cimport cos, sin, sqrt, acos
DEF pi = 3.141592653589793115997963468544185161590576171875
"""

from go.matrix44 import Matrix44


"""
cdef void _arg0(Quaternion self, args):
    self._t = 1.0
    self._x = 0.0
    self._y = 0.0
    self._z = 0.0
@cython.cdivision(True)
cdef void _arg1(Quaternion self, args):
    cdef double t, x, y, z, r
    t, x, y, z = args[0]
    r = t*t + x*x + y*y + z*z
    if r > 0.0:
        r = 1.0 / sqrt(r)
        self._t = t * r
        self._x = x * r
        self._y = y * r
        self._z = z * r
    else:
        self._t = 1.0
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
@cython.cdivision(True)
cdef void _arg2(Quaternion self, args):
    cdef double t, x, y, z, r
    t, (x, y, z) = args
    r = t*t + x*x + y*y + z*z
    if r > 0.0:
        r = 1.0 / sqrt(r)
        self._t = t * r
        self._x = x * r
        self._y = y * r
        self._z = z * r
    else:
        self._t = 1.0
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
@cython.cdivision(True)
cdef void _arg3(Quaternion self, args):
    cdef double x, y, z, r
    x, y, z = args
    r = x*x + y*y + z*z
    if r > 1.0:
        r = 1.0 / sqrt(r)
        self._t = 0.0
        self._x = x * r
        self._y = y * r
        self._z = z * r
    elif r > 0.0:
        self._t = 1.0 - sqrt(r)
        self._x = x
        self._y = y
        self._z = z
    else:
        self._t = 1.0
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
@cython.cdivision(True)
cdef void _arg4(Quaternion self, args):
    cdef double t, x, y, z, r
    t, x, y, z = args
    r = t*t + x*x + y*y + z*z
    if r > 0.0:
        r = 1.0 / sqrt(r)
        self._t = t * r
        self._x = x * r
        self._y = y * r
        self._z = z * r
    else:
        self._t = 1.0
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
cdef void (*_args[5])(Quaternion self, args)
_args[0] = _arg0
_args[1] = _arg1
_args[2] = _arg2
_args[3] = _arg3
_args[4] = _arg4
"""


class Quaternion:
    _t: float
    _x: float
    _y: float
    _z: float

    def __init__(self, *args) -> None: ...

    # TODO: should this be a static method? Why does it modify self?
    def from_floats(self, t: float, x: float, y: float, z: float) -> Quaternion:
        pass

    @classmethod
    def from_ax(cls, theta: float, ax: list[float]) -> Quaternion: ...

    @classmethod
    def from_RotMat(cls, R: Matrix44) -> Quaternion: ...

    def get_RotMat(self) -> Matrix44: ...

    def get_right_lis3_i(self) -> list[float]: ...
    def get_right_lis3(self) -> list[float]: ...

    def get_upward_lis3_i(self) -> list[float]: ...
    def get_upward_lis3(self) -> list[float]: ...

    def get_forward_lis3_i(self) -> list[float]: ...
    def get_forward_lis3(self) -> list[float]: ...

    def copy(self) -> Quaternion: ...
    __copy__ = copy

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    def __iter__(self):
        yield self._t
        yield self._x
        yield self._y
        yield self._z

    def __mul__(self, rhs: Quaternion) -> Quaternion: ...
    def __imul__(self, rhs: Quaternion) -> Quaternion: ...

    def get_spherep(self, othr: Quaternion, t: float) -> Quaternion: ...
