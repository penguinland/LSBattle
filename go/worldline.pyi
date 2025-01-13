# cython: profile=False
#cimport cython
#from libc.math cimport sqrt

#from go.vector4D cimport Vector4D

import collections.abc as c
import typing as t

from go.vector4D import Vector4D


class Cache:
    ix: int
    s: float
    def __init__(self) -> None: ...

class WorldLine:
    def __init__(self, P, Q=None) -> None:
        self.line: list[Vector4D] = [P.X.copy()]
        self.state: list[t.Any] = [Q]
        self.ix_map: c.Mapping[int, Cache] = {}
        self.n: int = 1
        self.last: int = -1

    def set_id(self, ix: int) -> None: ...

    def del_id(self, ix: int) -> None: ...

    def add(self, P: t.Any, Q: t.Optional[t.Any]) -> None: ...

    def cut(self) -> None: ...

    def search_position_on_PLC(self, Xp: Vector4D, ix: int) -> int: ...

    def get_X_FP(self, Xp_py: Vector4D, w: float) -> t.Optional[Vector4D]: ...

    def get_XU_on_PLC(self, Xp_py) -> tuple[t.Optional[Vector4D],
                                            t.Optional[Vector4D]]: ...

    def get_State_on_PLC(self, Xp_py) -> tuple[t.Any, t.Any, float]: ...

    def get_last(self) -> Vector4D: ...

    def __len__(self) -> int: ...
