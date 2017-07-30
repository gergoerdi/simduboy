from pysimavr.avr import Avr
from pysimavr.connect import avr_connect_irq
import pysimavr.swig.utils as utils
from pysimavr.swig.simavr import avr_raise_irq

from LCD import LCD

class Board:
    def __init__(self, avr):
        self.avr = avr

        self.lcd = LCD(self)
        avr_connect_irq(avr.irq.getioport(('D', 6)), self.lcd.sce)
        avr_connect_irq(avr.irq.getioport(('D', 4)), self.lcd.dc)
        avr_connect_irq(avr.irq.getioport(('D', 7)), self.lcd.reset)
        
        self.misoirq = avr.irq.getspi(0, utils.SPI_IRQ_INPUT)
        avr.irq.spi_register_notify(self.mosi)

    def miso(self, value):
        avr_raise_irq(self.misoirq, value)
        
    def mosi(self, irq, value):
        # print "MOSI: %02x" % value

        self.lcd.mosi(value)
        # self.ram.mosi(value)
        pass
