from typing import Iterator

from go.vector3 import Vector3


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

    t: float
    x: float
    y: float
    z: float
    d: Vector3

    def __iter__(self) -> Iterator[float]: ...

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
