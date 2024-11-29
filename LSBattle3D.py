#!/usr/bin/env python3
import os
import sys
import traceback

def log_error():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if os.name == "posix":
        p = os.path.dirname(sys.argv[0]) # app/Contants/MacOS
        p = os.path.dirname(p) # app/Contants/
        p = os.path.dirname(p) # app/
        p = os.path.dirname(p)
    else:
        p = os.path.dirname(sys.argv[0])
    p = os.path.join(p, "error.log")
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              file=open(p, "w")
                              )

try:
    import OpenGL
    OpenGL.ERROR_CHECKING = False
    # OpenGL.STORE_POINTERS = False
    # OpenGL.UNSIGNED_BYTE_IMAGES_AS_STRING = False
    import program.const
except:
    log_error()
    sys.exit(1)

def run():
    from sequence.game import Game
    game = Game()
    game.mainloop()

if __name__ == "__main__":
    try:
        run()
    except Exception:
        log_error()
        from program.box import BOX
        BOX.game_quit()
