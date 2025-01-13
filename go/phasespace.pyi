from go.vector4D import Vector4D
from go.matrix44 import Matrix44


class PhaseSpace:
    X: Vector4D
    U: Vector4D

    def __init__(self, X: Vector4D, U: Vector4D) -> None: ...

    def copy(self) -> PhaseSpace: ...

    def get_resist(self, b: float) -> Vector4D: ...

    def transform(self, acceleration: Vector4D, ds: float) -> None: ...
