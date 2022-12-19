#!/usr/bin/env python2

import sys
import ctypes
from sdl2 import *
import sdl2.ext
import array
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
    
    window = sdl2.ext.Window("Simduboy", size=(board.screen.WIDTH * 8, board.screen.HEIGHT * 8))
    renderer = SDL_CreateRenderer(window.window, -1, SDL_RENDERER_ACCELERATED)
    SDL_RenderSetLogicalSize(renderer, board.screen.WIDTH * 8, board.screen.HEIGHT * 8)

    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGB888, SDL_TEXTUREACCESS_STREAMING,
                                board.screen.WIDTH, board.screen.HEIGHT)

    window.show()

    while running:
        startTime = SDL_GetTicks()
        targetTime = startTime + (1000 / 60)
        
        pixbuf = board.screen.draw()
        buffer = (ctypes.c_uint32 * (board.screen.HEIGHT * board.screen.WIDTH))(*pixbuf)
        SDL_UpdateTexture(texture, None, buffer, board.screen.WIDTH * 4)
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, None)
        SDL_RenderPresent(renderer)

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
