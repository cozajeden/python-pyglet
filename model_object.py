from pyglet.gl import *
from line_object import Line
from poliline_object import Poliline
from rectangle_object import Rectangle
from pixel_object import Pixels
from spray_object import Spray

class Model:
    lines = list()
    polilines = list()
    rectangles = list()
    pixels = list()
    draws = list()
    draws_index = list()
    sprays = list()
    
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        
    def add_line(self, **kwargs):
        self.draws.append(Line(self.batch, **kwargs))
        return self.draws[-1]
    
    def add_lines(self, **kwargs):
        self.draws.append(Poliline(self.batch, **kwargs))
        return self.draws[-1]
    
    def add_rectangle(self, **kwargs):
        self.draws.append(Rectangle(self.batch, **kwargs))
        return self.draws[-1]
    
    def add_pixels(self, **kwargs):
        self.draws.append(Pixels(self.batch, **kwargs))
        return self.draws[-1]
    
    def add_spray(self, **kwargs):
        self.draws.append(Spray(self.batch, **kwargs))
        return self.draws[-1]
    
    def remove_last_draw(self):
        if len(self.draws): self.draws[-1].remove(); self.draws.pop();
            
    def remove_by_index(self, index):
        if len(self.draws): self.draws[index].remove(); self.draws.pop(index);
            
    def get_last_index(self):
        return len(self.draws) - 1
        
        
    def draw(self):
        self.batch.draw()