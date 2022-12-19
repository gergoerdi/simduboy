from pysimavr.avr import Avr
from pysimavr.swig.simavr import avr_alloc_irq, avr_raise_irq
from pysimavr.connect import avr_connect_irq
import pysimavr.swig.utils as utils
from pysimavr.swig.simavr import avr_raise_irq

from LCD import LCD
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

        self.lcd = LCD(self)
        avr_connect_irq(avr.irq.getioport(('D', 6)), self.lcd.sce)
        avr_connect_irq(avr.irq.getioport(('D', 4)), self.lcd.dc)
        avr_connect_irq(avr.irq.getioport(('D', 7)), self.lcd.reset)
        
        self.buttons = Buttons(self, self.keymap)

        self.misoirq = avr.irq.getspi(0, utils.SPI_IRQ_INPUT)
        avr.irq.spi_register_notify(self.mosi)

    def miso(self, value):
        avr_raise_irq(self.misoirq, value)
        
    def mosi(self, irq, value):
        # print "MOSI: %02x" % value

        self.lcd.mosi(value)
        # self.ram.mosi(value)
        pass

    def connect_input(self, pin):
        irq = avr_alloc_irq(self.avr.irq_pool, 0, 1, None)
        avr_connect_irq(irq, self.avr.irq.getioport(pin))
        return lambda(val): avr_raise_irq(irq, val)
    
