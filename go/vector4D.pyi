"""
# cython: profile=False
cimport cython
from libc.math cimport sqrt

from go.vector3 cimport vec3_from_floats
from go.vector4D cimport Vector4D, vec4_from_floats
"""


"""
cdef void _arg0(Vector4D self, args):
    self._t = 0.0
    self._x = 0.0
    self._y = 0.0
    self._z = 0.0
cdef void _arg1(Vector4D self, args):
    cdef double t, x, y, z
    t, x, y, z = args[0]
    self._t = t
    self._x = x
    self._y = y
    self._z = z
cdef void _arg2(Vector4D self, args):
    cdef double t, x, y, z
    t, (x, y, z) = args
    self._t = t
    self._x = x
    self._y = y
    self._z = z
cdef void _arg3(Vector4D self, args):
    cdef double x, y, z
    x, y, z = args
    self._t = 0.0
    self._x = x
    self._y = y
    self._z = z
cdef void _arg4(Vector4D self, args):
    cdef double t, x, y, z
    t, x, y, z = args
    self._t = t
    self._x = x
    self._y = y
    self._z = z
cdef void (*_args[5])(Vector4D self, args)
_args[0] = _arg0
_args[1] = _arg1
_args[2] = _arg2
_args[3] = _arg3
_args[4] = _arg4
"""

class Vector4D:

    def __init__(self, *args):
        _args[len(args)](self, args)

    @classmethod
    def from_tv(cls, t: float, v: float) -> Vector4D: ...

    def copy(self) -> Vector4D: ...
    __copy__ = copy

    """
    def _get_t(self):
        return self._t
    def _set_t(self, double t):
        self._t = t
    t = property(_get_t, _set_t, None, "t component.")

    def _get_x(self):
        return self._x
    def _set_x(self, double x):
        self._x = x
    x = property(_get_x, _set_x, None, "x component.")

    def _get_y(self):
        return self._y
    def _set_y(self, double y):
        self._y = y
    y = property(_get_y, _set_y, None, "y component.")

    def _get_z(self):
        return self._z
    def _set_z(self, double z):
        self._z = z
    z = property(_get_z, _set_z, None, "z component.")

    def _get_3d(self):
        return vec3_from_floats(self._x, self._y, self._z)
    def _set_3d(self, v):
        cdef double x, y, z
        x, y, z = v
        self._x = x
        self._y = y
        self._z = z
    d = property(_get_3d, _set_3d, None, "space part")
    """

    def __iter__(self):
        yield self._t
        yield self._x
        yield self._y
        yield self._z

    def __add__(lhs, rhs: Vector4D) -> Vector4D: ...
    def __iadd__(self, rhs: Vector4D) -> Vector4D: ...

    def __sub__(lhs, rhs: Vector4D) -> Vector4D: ...
    def __isub__(self, rhs: Vector4D) -> Vector4D: ...

    def __mul__(self, rhs: float) -> Vector4D: ...
    def __imul__(self, rhs: float) -> Vector4D: ...

    def __truediv__(self, rhs: float) -> Vector4D: ...
    def __itruediv__(self, rhs: float) -> Vector4D: ...

    def __neg__(self) -> Vector4D: ...

    def __pos__(self) -> Vector4D: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def length(self) -> float: ...

    def squared_length(self) -> float: ...

    def distance_to(self, othr: Vector4D) -> float: ...

    def distance_to_squared(self, othr: Vector4D) -> float: ...

    def dot(self, othr: Vector4D) -> float: ...

    def get_gamma(self) -> float: ...

    def inner_product(self, othr: Vector4D) -> float: ...

    def squared_norm(self) -> float: ...

    def squared_norm_to(self, othr: Vector4D) -> float: ...

    def get_hat(self, length: float) -> Vector4D: ...

    def hat(self, length: float) -> None: ...

    def get_normalize(self, length: float) -> Vector4D: ...

    def normalize(self, length: float) -> int: ...

    def get_linear_add(self, N: Vector4D, s: float) -> Vector4D: ...

    def get_linear_add_lis3(self, N: Vector4D, s: float) -> list[float]: ...

    def get_div_point(self, othr: Vector4D, s: float) -> Vector4D: ...

    def get_lis(self) -> list[float]: ...
    def get_lis_glsl(self) -> list[float]: ...
    def get_lis3(self) -> list[float]: ...

def vec4_from_floats(t: float, x: float, y: float, z: float) -> Vector4D: ...
