import os
import sys

# To import SDL2, we first set the $PYSDL2_DLL_PATH environment variable.
# It is either in resources/bin/posix/ (or resources/bin/nt), or else we'll try
# to find it in the topmost directory of the repo.
path = os.path.abspath(os.path.dirname(sys.argv[0]))
_input_path = os.path.join(path, "resources")
sdl2_path = os.path.join(_input_path, "bin", os.name)
if os.path.isdir(sdl2_path):
	os.environ["PYSDL2_DLL_PATH"] = sdl2_path
else:
	os.environ["PYSDL2_DLL_PATH"] = path

import sdl2

IMG_DIR    = os.path.join(_input_path, "img/")
CONFIG_DIR = os.path.join(_input_path, "config/")
SCRIPT_DIR = os.path.join(_input_path, "script/")

VIEW_ANGLE = 60.0
GAME_NAME = b"Light Speed Battle"

c = 299792458.0 #Light Speed [m/sec]

KS_RETURN = {sdl2.SDLK_RETURN, sdl2.SDLK_RETURN2, sdl2.SDLK_KP_ENTER}
KS_ESC = {sdl2.SDLK_ESCAPE, sdl2.SDLK_BACKSPACE, sdl2.SDLK_DELETE}

disp_sizes = [(640, 480),
              (800, 600),
              (1024, 768),
              (1280, 960),
              (1600, 1200)]
