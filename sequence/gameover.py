from OpenGL import GL
import sdl2

from program import script
from program.box import BOX
from program.const import KS_ESC, KS_RETURN
from sequence.locals import MenuItems


class GameOver(object):
    def __init__(self):
        self.lose_text = ["Game Over"]
        self.win_text = ["Game Clear!!"]

    def init(self, text):
        self.menu = MenuItems(text, BOX.Y / 8, 0.4)

    def mainloop(self, won=True):
        self.init(self.win_text if won else self.lose_text)
        start = sdl2.SDL_GetTicks()

        while True:
            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_QUIT:
                    BOX.game_quit()
                elif event.type == sdl2.SDL_KEYDOWN:
                    key = event.key.keysym.sym
                    if key in KS_ESC:
                        return
                    elif key in KS_RETURN:
                        return

            t = sdl2.SDL_GetTicks()
            if t - start > 2000:  # Two seconds have elapsed: move on.
                return

            GL.glClear(GL.GL_DEPTH_BUFFER_BIT|GL.GL_COLOR_BUFFER_BIT)
            self.menu.draw()
            sdl2.SDL_GL_SwapWindow(BOX.window)
            sdl2.SDL_Delay(10)
