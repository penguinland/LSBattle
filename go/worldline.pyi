from collections.abc import Mapping
from typing import Any, Optional

from go.vector4D import Vector4D


class Cache:
    ix: int
    s: float
    def __init__(self) -> None: ...

class WorldLine:
    def __init__(self, P, Q=None) -> None:
        self.line: list[Vector4D] = [P.X.copy()]
        self.state: list[Any] = [Q]
        self.ix_map: Mapping[int, Cache] = {}
        self.n: int = 1
        self.last: int = -1

    def set_id(self, ix: int) -> None: ...

    def del_id(self, ix: int) -> None: ...

    def add(self, P: Any, Q: Optional[Any]) -> None: ...

    def cut(self) -> None: ...

    def search_position_on_PLC(self, Xp: Vector4D, ix: int) -> int: ...

    def get_X_FP(self, Xp_py: Vector4D, w: float) -> Optional[Vector4D]: ...

    def get_XU_on_PLC(self, Xp_py) -> tuple[Optional[Vector4D],
                                            Optional[Vector4D]]: ...

    def get_State_on_PLC(self, Xp_py) -> tuple[Any, Any, float]: ...

    def get_last(self) -> Vector4D: ...

    def __len__(self) -> int: ...
