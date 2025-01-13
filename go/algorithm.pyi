"""
# cython: profile=False
cimport cython
from libc.math cimport sqrt
"""

import typing as t

from go.vector4D import Vector4D
from go.matrix44 import Matrix44


def calc_shoot_direction(Xp: Vector4D, Up: Vector4D, X: Vector4D, U: Vector4D,
                         v: float) -> t.Optional[list[float]]: ...


def calc_repulsion(Xp: Vector4D, X1: Vector4D, U1: Vector4D, collision_radius:
                   float, repulsion: float, acceleration: Vector4D) -> None: ...


# TODO: should this return 0 instead of None in the bad case?
def hit_check(Xs: Vector4D, N: Vector4D, S: float, X1: Vector4D, X0: Vector4D,
              collision_radius2: float) -> t.Optional[float]: ...
