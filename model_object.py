from pyglet.gl import *
from rectangle_object import Rectangle
from polyline_object import Polyline
from polygon_object import Polygon
from circle_object import Circle
from pixel_object import Pixels
from spray_object import Spray
from line_object import Line

class Model:
    draws = list()
    
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        
    def add_rectangle(self, **kwargs): self.draws.append(Rectangle(self.batch, **kwargs)); return self.draws[-1]
    def add_polyline(self, **kwargs):  self.draws.append(Polyline(self.batch, **kwargs));  return self.draws[-1]
    def add_polygon(self, **kwargs):   self.draws.append(Polygon(self.batch, **kwargs));   return self.draws[-1]
    def add_circle(self, **kwargs):    self.draws.append(Circle(self.batch, **kwargs));    return self.draws[-1]
    def add_pixels(self, **kwargs):    self.draws.append(Pixels(self.batch, **kwargs));    return self.draws[-1]
    def add_spray(self, **kwargs):     self.draws.append(Spray(self.batch, **kwargs));     return self.draws[-1]
    def add_line(self, **kwargs):      self.draws.append(Line(self.batch, **kwargs));      return self.draws[-1]
    
    def remove_last_draw(self):
        if len(self.draws): self.draws[-1].remove(); self.draws.pop()
            
    def remove_by_index(self, index, update=None):
        if len(self.draws): self.draws[index].remove(); self.draws.pop(index)
        if update: return self.update_index_list(update, index)
            
    def get_last_index(self):
        return len(self.draws) - 1
        
    def update_index_list(self, update, index=0):
        return update[:index] + list(map(lambda x: x-1, update[index:]))
        
    def draw(self):
        self.batch.draw()
            