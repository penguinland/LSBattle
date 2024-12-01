from math import sqrt, sin, cos, pi, tau
from random import uniform

from go import Vector4D, Lorentz
from model.pointsprite import PointSprite
from program.box import BOX
from program.utils import DY_TEXTURE_KYU


class Flame(object):
    def __init__(self, S=0.5, v=0.6, n=5, m=10,
                 color=(1.0, 0.9, 0.99, 0.6), psize=0.02):
        """
        S: float, lifetime of each particle consisting of the flame.
        v: float, velocity of each particle consisting of the flame.
        n: int, number of particles in zenith angle direction.
        m: int, number of particles in azimuthal angle direction.
        psize: float, size of each particle consisting of the flame, relative to screen size.
        """
        self.model = PointSprite(color=color, texture=DY_TEXTURE_KYU)
        t = 1.0/v

        # We use polar coordinates to create a bunch of vertices. Put one at the
        # north pole, then rings along lines of latitude, and finally one at the
        # south pole.
        vertices = [Vector4D(t, 0.0, 1.0, 0.0)]
        for i in range(1, m):  # 0 through m, not including 0 or m itself
            phi = pi * i / m
            # To stagger the particles, every other one will be rotated half a
            # line of longitude off from the previous/next row.
            offset = 0.5 if (i % 2 == 1) else 0.0
            for j in range(n):
                theta = tau * (j + offset) / n
                vertices.append(Vector4D(t, sin(phi)*sin(theta),
                                            cos(phi),
                                            sin(phi)*cos(theta)))
        vertices.append(Vector4D(t, 0.0, -1.0, 0.0))

        self.vertices = vertices
        self.a = self.vertices[0].squared_norm()
        # Give each vertex a small random variation in the size
        ideal_size = BOX.Y * psize
        self.sizes = [ideal_size * uniform(0.9, 1.1) for _ in self.vertices]
        self.SS = [S * uniform(0.5, 2.5) for _ in self.vertices]

    def draw(self, X, Xp, L, LL=None, color=None):
        """
        We return whether we drew any flames (whether any of the particles has
        not yet reached the end of its life).
        """
        a = self.a
        dX = (Xp - X)*(1.0/a)
        c = dX.squared_norm()
        ac = a * c
        vertices = []
        U = []
        sizes = []
        if LL is None:
            NN = self.vertices
        else:
            NN = [LL.get_transform(N) for N in self.vertices]

        vc = 0  # Count of non-positive s 
        for N, S, size in zip(NN, self.SS, self.sizes):
            b = N.inner_product(dX)
            s = b - sqrt(b*b - ac)
            if 0.0 < s:
                if s < S:
                    vertices.extend(X.get_linear_add_lis3(N, s))
                    U.extend(N.get_lis_glsl())
                    sizes.append(size)
            else:
                vc += 1

        if vertices:
            self.model.draw(Xp, L, vertices, U, sizes, color=color)
            return True
        return (vc == 0)  # whether any s was non-positive
