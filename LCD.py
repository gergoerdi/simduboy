import sdl2.ext
from pysimavr.swig.simavr import avr_alloc_irq

class LCD:
    WIDTH = 128
    HEIGHT = 64

    FG_COLOR = sdl2.ext.Color(0xff, 0xe0, 0xe0, 0xe0)
    BG_COLOR = sdl2.ext.Color(0xff, 0x10, 0x10, 0x10)
    
    def __init__(self, board):
        self.board = board

        self.sce = avr_alloc_irq(board.avr.irq_pool, 0, 1, None)
        self.dc = avr_alloc_irq(board.avr.irq_pool, 0, 1, None)
        self.reset = avr_alloc_irq(board.avr.irq_pool, 0, 1, None)
        
        self.dirty = False
        self.framebuf = [[False for i in range(self.HEIGHT)] for i in range(self.WIDTH)]
        self.nextXY = (0, 0)

    def draw(self, pixels):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                pixels[y * self.WIDTH + x] = int(self.FG_COLOR if self.framebuf[x][y] else self.BG_COLOR)
        pass
        

    def mosi(self, value):
        if self.sce.value != 0:
            return
            
        if self.dc.value == 0:
            print "Command to LCD: 0x%02x" % value
            pass
        else:
            (x, y) = self.nextXY
            for i in range(8):
                self.framebuf[x][y + i] = value & 0x01
                value = value >> 1
            self.dirty = True

            x = x + 1
            if x >= self.WIDTH:
                (x, y) = (0, y + 8)
            if y >= self.HEIGHT:
                (x, y) = (0, 0)
            self.nextXY = (x, y)

