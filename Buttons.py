from sdl2 import *

import sys

class Buttons:
    keymap = [ (SDL_SCANCODE_UP,     ('F', 7)),
               (SDL_SCANCODE_DOWN,   ('F', 4)),
               (SDL_SCANCODE_LEFT,   ('F', 5)),
               (SDL_SCANCODE_RIGHT,  ('F', 6)),
               (SDL_SCANCODE_LCTRL,  ('E', 6)),
               (SDL_SCANCODE_LSHIFT, ('B', 4)) ]

    def __init__(self, board):
        self.btns = [(scancode, board.connect_input(pin)) for (scancode, pin) in self.keymap]

    def set_keystate(self, keystate):
        for (scancode, irq) in self.btns:
            irq(0 if keystate[scancode] else 1)
