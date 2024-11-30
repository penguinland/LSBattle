from math import pi

from ..common import Block, color_func, high_func_num, parse_string


class sky(Block):
    def __init__(self):
        self.texture0 = "milkyway.jpg"
        self.texture1 = "milkyway2.jpg"
        self.rotation0 = 90.0
        self.rotation1 = 30.0
        self._texture0_func = parse_string
        self._texture1_func = parse_string
        self._rotation0_func = high_func_num(float, -180, 180)
        self._rotation1_func = high_func_num(float, -180, 180)
