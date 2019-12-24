from pyglet.gl import *
from line_object import Line
from rectangle_object import Rectangle
from pixel_object import Pixels
from spray_object import Spray

class Model:
    lines = list()
    rectangles = list()
    pixels = list()
    draws = list()
    sprays = list()
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        
    
    def add_blue_pixel(self, x, y):
        self.vertex_list = self.batch.add(1, GL_POINTS, None,
                                ('v2i', (x, y)),
                                ('c3B', (0, 0, 255)))
    
    def add_line(self, **kwargs):
        self.lines.append(Line(self.batch, **kwargs))
        self.draws.append(self.lines[-1])
        return self.lines[-1]
    
    def add_rectangle(self, **kwargs):
        self.rectangles.append(Rectangle(self.batch, **kwargs))
        self.draws.append(self.rectangles[-1])
        return self.rectangles[-1]
    
    def add_pixels(self, **kwargs):
        self.pixels.append(Pixels(self.batch, **kwargs))
        self.draws.append(self.pixels[-1])
        return self.pixels[-1]
    
    def add_spray(self, **kwargs):
        self.sprays.append(Spray(self.batch, **kwargs))
        self.draws.append(self.sprays[-1])
        return self.sprays[-1]
    
    def remove_last_draw(self):
        if len(self.draws):
            if   isinstance(self.draws[-1], Spray):     self.draws[-1].remove(); self.draws.pop(); self.sprays.pop()
            elif isinstance(self.draws[-1], Pixels):    self.draws[-1].remove(); self.draws.pop(); self.pixels.pop()
            elif isinstance(self.draws[-1], Line):      self.draws[-1].remove(); self.draws.pop(); self.lines.pop()
            elif isinstance(self.draws[-1], Rectangle): self.draws[-1].remove(); self.draws.pop(); self.rectangles.pop()
        
    def draw(self):
        self.batch.draw()