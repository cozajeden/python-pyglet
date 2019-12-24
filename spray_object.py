from pyglet.gl import *
from pixel_object import Pixels
from random import random
from numpy import sin, cos, pi

class Spray(Pixels):
    def __init__(self, batch, position, intensity=10, radius=10, color=[555]*3):
        self.radius = radius
        self.intensity = intensity
        super().__init__(batch, *self.calculate_positions(position, intensity, radius, color))
        
    def update(self, position, color=None):
        if not color:
            color = self.color[-3:]
        super().update(None, *self.calculate_positions(position, self.intensity, self.radius, color), True)
        
    def calculate_positions(self, position, intensity, radius, color):
        _position = []
        _color = []
        for i in range(intensity):
            rand = random()*2*pi
            x = cos(rand)*random()*radius
            y = sin(rand)*random()*radius
            _position.extend([position[0] + x, position[1] + y])
            _color.extend(color)
        return _position, _color