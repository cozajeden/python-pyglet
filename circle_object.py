from pyglet.gl import *
from polygon_object import Polygon
from numpy import pi, sin, cos, sqrt
from random import random

class Circle(Polygon):
    def __init__(self, batch, position, radius, color=None, group=None):
        self.radius = radius
        if not color:
            color = [255]*6
        self.calculate(position, radius, color)
        super().__init__(batch, self.position, self.color, group)
        
    def draw(self):
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.vertex = self.batch.add(int(len(self.position)/2), GL_TRIANGLE_FAN, self.group,
                                ('v2f', self.position), 
                                ('c3B', self.color))
    
    def calculate(self, position, radius, color):
        self.position = position
        interval = int(2*pi*radius)
        interval = list(map(lambda i: 2*pi*i/interval, range(interval + 1)))
        for i in interval:
            self.position.extend([cos(i)*radius + self.position[0], sin(i)*radius + self.position[1]])
        self.color = color[:3] + color[3:]*len(interval)
        
    def update(self, position=None, radius=None, on_circumference_point=None, color=None):
        if not color:
            color = self.color[:6]
        if position and radius:
            pass
        elif position and on_circumference_point:
            radius = sqrt(abs(position[0] - on_circumference_point[0])**2 + abs(position[1] - on_circumference_point[1])**2)
        elif radius:
            position = self.position[:2]
        elif on_circumference_point:
            radius = sqrt(abs(self.position[0] - on_circumference_point[0])**2 + abs(self.position[1] - on_circumference_point[1])**2)
            position = self.position[:2]
        elif position:
            radius = self.radius
        self.calculate(position, radius, color)
        self.draw()
        
        
    def extend(self):
        "This function do nothing."
        del self.extend