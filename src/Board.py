from pysimavr.avr import Avr
from pysimavr.swig.simavr import avr_alloc_irq, avr_raise_irq
from pysimavr.connect import avr_connect_irq
import pysimavr.swig.utils as utils

from Screen import Screen
from Buttons import Buttons
from sdl2 import *

class Board:
    keymap = [ (SDL_SCANCODE_UP,     ('F', 7)),
               (SDL_SCANCODE_DOWN,   ('F', 4)),
               (SDL_SCANCODE_LEFT,   ('F', 5)),
               (SDL_SCANCODE_RIGHT,  ('F', 6)),
               (SDL_SCANCODE_LCTRL,  ('E', 6)),
               (SDL_SCANCODE_LSHIFT, ('B', 4)) ]

    def __init__(self, avr):
        self.avr = avr
        self.mosi_callbacks = []

        self.screen = Screen(self)
        self.connect_output(('D', 6), lambda(v): setattr(self.screen, 'sce', v))
        self.connect_output(('D', 4), lambda(v): setattr(self.screen, 'dc', v))
        self.connect_output(('D', 7), lambda(v): setattr(self.screen, 'reset', v))
        
        self.buttons = Buttons(self, self.keymap)

        self.misoirq = avr.irq.getspi(0, utils.SPI_IRQ_INPUT)
        avr.irq.spi_register_notify(self.mosi)

    def miso(self, value):
        avr_raise_irq(self.misoirq, value)
        
    def mosi(self, irq, value):
        # print "MOSI: %02x" % value

        for cb in self.mosi_callbacks:
            cb(value)

    def connect_input(self, pin):
        irq = avr_alloc_irq(self.avr.irq_pool, 0, 1, None)
        avr_connect_irq(irq, self.avr.irq.getioport(pin))
        return lambda(val): avr_raise_irq(irq, val)

    def connect_output(self, pin, listener):
        irq = avr_alloc_irq(self.avr.irq_pool, 0, 1, None)
        self.avr.irq._register_callback(irq, lambda irq, value: listener(value), True)
        avr_connect_irq(self.avr.irq.getioport(pin), irq)

    def connect_mosi(self, cb):
        self.mosi_callbacks += [cb]
