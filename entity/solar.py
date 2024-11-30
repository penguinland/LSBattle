from math import pi, sin, cos

from OpenGL.GL import *

from go import Matrix44, Vector4D, Lorentz, calc_repulsion
from model.flame import Flame
from model.polygon import Polygon
from program import script
from program.box import BOX
from program.const import IMG_DIR, c
from program.text import drawSentence3d


def _calc_star_pos(Xp, scale, star_datum):
    """
    We return a dict from star names to (4D) locations. The names come from
    star_datum, and the locations are offset and scaled by Xp and scale.
    """
    def calc_pos(r, phi):  # Helper
        cos_p = cos(phi * pi / 180)
        sin_p = sin(phi * pi / 180)
        return Vector4D(0.0, sin_p * r, 0.0, cos_p * r)

    # Map from names of celestial bodies to their initial positions
    star_pos = {}

    # Initialize the star in the center of the map. All other stars will
    # somehow be placed relative to this one.
    center = script.world.solar.center.lower()
    if center not in star_datum:
        if "sun" not in star_datum:
            return
        else:
            center = "sun"
    offset = Vector4D(0.0,
                      script.world.solar.dx,
                      script.world.solar.dy,
                      script.world.solar.dz) * scale
    star_pos[center] = Xp + offset

    # We now put in all the other celestial bodies. They all have positions
    # relative to others: now that the center star is in, repeatedly put in all
    # stars that define themselves relative to a previously-placed star or
    # have a previously-placed star defined relative to themselves.
    making_progress = True
    while making_progress:
        making_progress = False
        for name, star_data in star_datum.items():
            if name in star_pos:  # Already finished with this one last time
                continue

            # See if the parent of this star is already set up.
            if star_data.primary_star is not None:
                pname = star_datum[star_data.primary_star].name
                if pname in star_pos:
                    # The parent star is already initialized; put this one
                    # at the right offset from it.
                    pos = calc_pos(star_data.orbital_radius,
                                   star_data.orbital_phi)
                    star_pos[name] = star_pos[pname] + pos
                    making_progress = True
                    continue

            # See if any child of this star is already set up.
            for sname in star_pos:
                sdata = star_datum[sname]
                if name == sdata.primary_star:
                    pos = calc_pos(sdata.orbital_radius,
                                   sdata.orbital_phi)
                    star_pos[name] = star_pos[sname] - pos
                    making_progress = True
                    break
    return star_pos


def _high_func(sphere_radius, tilt):
    """
    Returns a function that scales and rotates points by the given radius and
    tilt. The tilt is given in degrees!
    """
    mat = (Matrix44.scale(sphere_radius) *
           Matrix44.z_rotation(tilt * pi / 180) *
           Matrix44.y_rotation(pi / 2))
    def func(x, y, z):
        return mat.get_rotate([x, y, z])
    return func


class Star(object):
    def __init__(self, X, star_data):
        func = _high_func(star_data.sphere_radius, star_data.tilt)
        self.radius = star_data.sphere_radius
        self.radius2 = self.radius ** 2
        model_location = IMG_DIR + star_data.model
        if star_data.texture is None:
            self.model = Polygon(model_location, func=func)
        else:
            self.model = Polygon(model_location, func=func, texture=False)
            self.model.set_texture(star_data.texture)
        self.X = X.copy()
        self.hp = star_data.hp
        flame_data = script.world.solar.flame
        self.flame = Flame(S=flame_data.life * self.radius,
                           v=flame_data.speed,
                           n=flame_data.num,
                           m=flame_data.num * 2,
                           color=flame_data.color,
                           psize=flame_data.size * self.radius)
        self.alive = True
        self.X_dead = None

    def draw(self, Xp, L, LL):
        if self.hp <= 0:
            if not self.flame.draw(self.X_dead, Xp, L):
                # All flame particles have burned out
                self.alive = False
            return

        dX = self.X - Xp
        dX.t = -dX.length()
        dx = L.get_transform(dX)
        r = -dx.t
        if r > 0.5 * BOX.far_clip:
            s = 0.05 * BOX.far_clip / r
            X = Xp + dX * s
            self.model.draw(Xp, L, LL, X=X, R=Matrix44.scale(s))
        else:
            self.model.draw(Xp, L, LL, X=self.X)

    def hit_check(self, Xp, world):
        if self.hp <= 0:
            return

        t = Xp.t - Xp.distance_to(self.X)
        self.X.t = t
        X1 = self.X + Vector4D(0.02, 0, 0, 0)
        self.hp -= world.player.bullet_hit_check(X1, self.X, self.radius2)
        self.hp -= world.enemies.bullets.hit_check(X1, self.X, self.radius2)
        if self.hp <= 0:
            self.X_dead = self.X.copy()


class SolarSystem(object):
    star_datum = None

    def __init__(self, world, Xp, scale):
        self.world = world
        self.stars = {}

        # Try to initialize star_datum
        self.read_data()
        if not self.star_datum:
            return

        self.star_pos = _calc_star_pos(Xp, scale, self.star_datum)
        self.stars = {name: Star(pos, self.star_datum[name])
                      for name, pos in self.star_pos.items()}

    @classmethod
    def read_data(cls):
        if cls.star_datum is not None:
            return
        rescale = 1.0 / c
        cls.star_datum = {}
        # TODO: where is this!? I can't find stars in
        # program/script/world/solar.py
        for star_data in script.world.solar.stars:
            star_data.sphere_radius *= rescale
            star_data.orbital_radius *= rescale
            star_data.name = star_data.name.lower()
            pname = star_data.primary_star
            star_data.primary_star = pname.lower() if pname is not None else None
            cls.star_datum[star_data.name] = star_data

    def __getitem__(self, key):
        return self.stars[key]

    def __iter__(self):
        for name in self.stars:
            yield self.stars[name]

    def draw(self, Xp, L, LL):
        for star in self.stars.values():
            star.draw(Xp, L, LL)

    def hit_check(self, Xp):
        for star in self.stars.values():
            if star.hp > 0:
                star.hit_check(Xp, self.world)

    def calc_repulsion(self, Xp, acceleration, collision_radius, repulsion):
        U = Vector4D(1.0, 0.0, 0.0, 0.0)
        for star in self.stars.values():
            if star.hp > 0:
                star.X.t = Xp.t - Xp.distance_to(star.X)
                calc_repulsion(Xp, star.X, U,
                               collision_radius + star.radius,
                               repulsion,
                               acceleration)
