from pyglet.gl import *
from polyline_object import Polyline

class Polygon(Polyline):
    def draw(self):
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.vertex = self.batch.add(int(len(self.position)/2), GL_POLYGON, None,
                                ('v2f', self.position), 
                                ('c3B', self.color))
        
    def extend(self, position, color=[255]*3):
        self.color += color
        self.position.extend(position)
        self.draw()