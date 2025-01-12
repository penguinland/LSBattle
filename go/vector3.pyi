"""
# cython: profile=False
cimport cython
from libc.math cimport sqrt

from go.vector3 cimport Vector3, vec3_from_floats
"""


def _arg0(self: Vector3, args) -> None: ...
def _arg1(self: Vector3, args) -> None: ...
def _arg3(self: Vector3, args) -> None: ...
# _args is an array of 4 function pointers, each of which takes self and args
# and returns void.
"""
cdef void (*_args[4])(Vector3 self, args)
_args[0] = _arg0
_args[1] = _arg1
_args[2] = NULL  # No constructor takes 2 args.
_args[3] = _arg3
"""


class Vector3:
    # TODO
    def __init__(self, *args):
        _args[len(args)](self, args)

    def copy(self) -> Vector3: ...
    # TODO
    __copy__ = copy

    """
    # TODO
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
    """

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    # TODO
    def __iter__(self):
        yield self._x
        yield self._y
        yield self._z

    def __add__(self, rhs: Vector3) -> Vector3: ...
    def __iadd__(self, rhs: Vector3)-> Vector3: ...

    def __sub__(self, rhs: Vector3) -> Vector3: ...
    def __isub__(self, rhs: Vector3) -> Vector3: ...

    def __mul__(self, rhs: float) -> Vector3: ...
    def __imul__(self, rhs: float) -> Vector3: ...

    def __truediv__(self, rhs: float) -> Vector3: ...
    def __itruediv__(self, rhs: float) -> Vector3: ...

    def __neg__(self) -> Vector3: ...

    def __pos__(self) -> Vector3: ...

    def get_hat(self, length: float) -> Vector3: ...

    def hat(self, length: float) -> None: ...

    def get_normalize(self, length: float) -> Vector3: ...

    def normalize(self, length: float) -> None: ...

    def length(self) -> float: ...

    def squared_length(self) -> float: ...

    def distance_to(self, othr: Vector3) -> float: ...

    def distance_to_squared(self, othr: Vector3) -> float: ...

    def dot(self, othr: Vector3) -> float: ...

    def cross(self, othr: Vector3) -> Vector3: ...

    def get_lis(self) -> list[float]: ...

def vec3_from_floats(x: float, y: float, z: float) -> Vector3: ...
