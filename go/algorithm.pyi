from typing import Optional

from go.vector4D import Vector4D


def calc_shoot_direction(Xp: Vector4D, Up: Vector4D, X: Vector4D, U: Vector4D,
                         v: float) -> Optional[list[float]]: ...


def calc_repulsion(Xp: Vector4D, X1: Vector4D, U1: Vector4D, collision_radius:
                   float, repulsion: float, acceleration: Vector4D) -> None: ...


# TODO: should this return 0 instead of None in the bad case?
def hit_check(Xs: Vector4D, N: Vector4D, S: float, X1: Vector4D, X0: Vector4D,
              collision_radius2: float) -> Optional[float]: ...
