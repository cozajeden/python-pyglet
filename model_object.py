from pyglet.gl import *
import re
from rectangle_object import Rectangle
from polyline_object import Polyline
from polygon_object import Polygon
from sprite_object import Sprite
from circle_object import Circle
from pixel_object import Pixels
from spray_object import Spray
from line_object import Line

class Model:
    draws = list()
    
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.tools = {
            'Rectangle': Rectangle,
            'Polyline': Polyline,
            'Polygon': Polygon,
            'Sprite': Sprite,
            'Circle': Circle,
            'Pixels': Pixels,
            'Spray': Spray,
            'Line': Line
        }
        
    def add_rectangle(self, **kwargs): self.draws.append(Rectangle(self.batch, **kwargs)); return self.draws[-1]
    def add_polyline(self, **kwargs):  self.draws.append(Polyline(self.batch, **kwargs));  return self.draws[-1]
    def add_polygon(self, **kwargs):   self.draws.append(Polygon(self.batch, **kwargs));   return self.draws[-1]
    def add_sprite(self, **kwargs):    self.draws.append(Sprite(self.batch, **kwargs));    return self.draws[-1]
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
        
    def move_draws(self, x=0, y=0, z=0, indexes=[-1], origin=[0, 0]):
        for index, each in enumerate(self.draws):
            if indexes[0] == -1 or index in indexes:
                if x:
                    each.position = list(map(lambda n: n[1]+x if not n[0]%2 else n[1], enumerate(each.position)))
                if y:
                    each.position = list(map(lambda n: n[1]+y if n[0]%2 else n[1], enumerate(each.position)))
                if z:
                    if isinstance(z, list):
                        each.position = list(map(lambda n: (n[1]-origin[0])*(1 + z[0])+origin[0] if not n[0]%2 else n[1], enumerate(each.position)))
                        each.position = list(map(lambda n: (n[1]-origin[1])*(1 + z[1])+origin[1] if n[0]%2 else n[1], enumerate(each.position)))
                    else:
                        each.position = list(map(lambda n: (n[1]-origin[0])*(1 + z)+origin[0] if not n[0]%2 else n[1], enumerate(each.position)))
                        each.position = list(map(lambda n: (n[1]-origin[1])*(1 + z)+origin[1] if n[0]%2 else n[1], enumerate(each.position)))
            if x or y or z: each.hide(); each.draw()
            
    def save(self, path):
        types = str(self.draws).split()[::4]
        types = list(map(lambda line: line[line.find('.') + 1:], types))
        attributes = []
        for index, item in enumerate(types):
            attributes.append([item])
            attributes[-1].append(self.draws[index].position)
            if item not in ('Sprite'): attributes[-1].append(self.draws[index].color)
            else: attributes[-1].append(self.draws[index].path)
            attributes[-1].append(re.search('[0-9]+', str(self.draws[index].group)).group(0))
            if item in ('Circle', 'Spray'):
                attributes[-1].append(self.draws[index].radius)
            if item == 'Spray':
                attributes[-1].append(self.draws[index].intensity)
        with open(path, 'w') as f:
            f.write(str(attributes))
            
    def load(self, path):
        with open(path, 'r') as f:
            attributes = eval(f.read())
        for item in attributes:
            arguments = {
                'position': item[1],
                'group': pyglet.graphics.OrderedGroup(int(item[3]))
            }
            if item[0] not in ('Sprite'): arguments['color'] = item[2]
            else: arguments['path'] = item[2]
            if item[0] in ('Circle', 'Spray'): arguments['radius'] = item[4]; arguments['load'] = True
            if item[0] in ('Spray'):           arguments['intensity'] = item[5]
            self.draws.append(self.tools[item[0]](self.batch, **arguments))