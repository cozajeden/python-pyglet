from pyglet.gl import *
from line_object import Line
from rectangle_object import Rectangle

class Model:
    lines = list()
    rectangles = list()
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        
    
    def add_blue_pixel(self, x, y):
        self.vertex_list = self.batch.add(1, GL_POINTS, None,
                                ('v2i', (x, y)),
                                ('c3B', (0, 0, 255)))
    
    def add_line(self, **kwargs):
        self.lines.append(Line(self.batch, **kwargs))
        return self.lines[-1]
    
    def add_rectangle(self, **kwargs):
        self.rectangles.append(Rectangle(self.batch, **kwargs))
        return self.rectangles[-1]
        
    def draw(self):
        self.batch.draw()