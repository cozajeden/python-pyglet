from pyglet.gl import *
from polyline_object import Polyline

class Polygon(Polyline):
    def draw(self):
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.vertex = self.batch.add(int(len(self.position)/2), GL_POLYGON, self.group,
                                ('v2f', self.position), 
                                ('c3B', self.color))
        
    def extend(self, position, color=None, update=False):
        if not update:
            if not color:
                color = [255]*3
            self.color += color
            self.position.extend(position)
        else:
            self.position = self.position[:-2] + position
        self.draw()