#!/usr/bin/env python

import sys
import ctypes
from sdl2 import *
import sdl2.ext
import ctypes

from pysimavr.avr import Avr
from pysimavr.firmware import Firmware

from Board import Board
    
def main():
    avr = Avr(mcu='atmega32u4',f_cpu=16000000)
    firmware = Firmware('image.elf')
    avr.load_firmware(firmware)
    
    board = Board(avr)

    running = True
    
    sdl2.ext.init()
    
    window = sdl2.ext.Window("Simduboy", size=(board.lcd.WIDTH * 8, board.lcd.HEIGHT * 8))
    renderer = SDL_CreateRenderer(window.window, -1, SDL_RENDERER_ACCELERATED)
    SDL_RenderSetLogicalSize(renderer, board.lcd.WIDTH * 8, board.lcd.HEIGHT * 8)

    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGB888, SDL_TEXTUREACCESS_STREAMING,
                                board.lcd.WIDTH, board.lcd.HEIGHT)

    window.show()

    while running:
        targetTime = SDL_GetTicks() + 17
        
        pixbuf = board.lcd.draw()
        buffer = (ctypes.c_uint32 * (board.lcd.HEIGHT * board.lcd.WIDTH))(*pixbuf)
        SDL_UpdateTexture(texture, None, buffer, board.lcd.WIDTH * 4)
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, None)
        SDL_RenderPresent(renderer)

        events = sdl2.ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            # elif event.type in [SDL_KEYDOWN, SDL_KEYUP]:
            #     board.keypad.keypress(event.key.keysym.scancode, event.key.state == SDL_PRESSED)

        while SDL_GetTicks() < targetTime:
            avr.run()

    sdl2.ext.quit()
    return 0    

if __name__ == "__main__":
    sys.exit(main())
