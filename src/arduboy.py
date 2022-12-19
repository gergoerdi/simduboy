#!/usr/bin/env python2

import argparse

import sys
from sdl2 import *
import sdl2.ext

from pysimavr.avr import Avr
from pysimavr.firmware import Firmware

from Board import Board
from Screen import Screen
from Buttons import Buttons

class Arduboy(Board):
    keymap = [ (SDL_SCANCODE_UP,     ('F', 7)),
               (SDL_SCANCODE_DOWN,   ('F', 4)),
               (SDL_SCANCODE_LEFT,   ('F', 5)),
               (SDL_SCANCODE_RIGHT,  ('F', 6)),
               (SDL_SCANCODE_LCTRL,  ('E', 6)),
               (SDL_SCANCODE_LSHIFT, ('B', 4)) ]

    def __init__(self, avr):
        Board.__init__(self, avr)

        self.screen = Screen(self)
        self.connect_output(('D', 6), lambda(v): setattr(self.screen, 'sce', v))
        self.connect_output(('D', 4), lambda(v): setattr(self.screen, 'dc', v))
        self.connect_output(('D', 7), lambda(v): setattr(self.screen, 'reset', v))

        self.buttons = Buttons(self, self.keymap)

def main():
    parser = argparse.ArgumentParser(
        description='Arduboy Simulator',
        usage="%(prog)s IMAGE.elf")
    parser.add_argument('filename', metavar='IMAGE.elf', help='Path to .elf file')
    args = parser.parse_args()
    
    avr = Avr(mcu='atmega32u4',f_cpu=16000000)
    firmware = Firmware(args.filename)
    avr.load_firmware(firmware)

    sdl2.ext.init()

    board = Arduboy(avr)

    running = True
    while running:
        startTime = SDL_GetTicks()
        targetTime = startTime + (1000 / 60)

        board.screen.draw()
        drawTime = SDL_GetTicks()

        events = sdl2.ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            elif event.type == SDL_KEYDOWN and event.key.keysym.scancode == SDL_SCANCODE_ESCAPE:
                running = False
                break
        board.buttons.set_keystate(SDL_GetKeyboardState(None))

        while SDL_GetTicks() < targetTime:
            avr.run()

    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
