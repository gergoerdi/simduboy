import sys

class Buttons:
    def __init__(self, board, keymap):
        self.btns = [(scancode, board.connect_input(pin)) for (scancode, pin) in keymap]

    def set_keystate(self, keystate):
        for (scancode, irq) in self.btns:
            irq(0 if keystate[scancode] else 1)
