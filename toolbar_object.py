from pyglet.gl import *
from rectangle_object import Rectangle

class Toolbar:
    def __init__(self, batch, x, y, x2, y2, group=None):
        self.group = group
        self.batch = batch
        self.update_position(x, y, x2, y2)
        self.blue_color = [0]*5 + [255] + [0]*2 + [255] + [0]*3
        self.green_color = [0]*4 + [255] + [0]*2 + [255] + [0]*4
        self.red_color = [0]*3 + [255] + [0]*2 + [255] + [0]*5
        self.front_color = [255]*12
        self.back_color = [0]*12
        self.choosen = 0
        self.blue = Rectangle(self.batch, *self.blue_position, self.blue_color, self.group)
        self.green = Rectangle(self.batch, *self.green_position, self.green_color, self.group)
        self.red = Rectangle(self.batch, *self.red_position, self.red_color, self.group)
        self.front = Rectangle(self.batch, *self.front_color_position, self.front_color, self.group)
        self.back = Rectangle(self.batch, *self.back_color_position, self.back_color, self.group)
        
    def on_mouse_press(self, x, y):
        for i, r in enumerate(self.rectangles):
            if (r[0] < x < r[2]) and (r[1] < y < r[3]):
                if   i == 0: self.choosen = 0
                elif i == 1: self.choosen = 1
                elif i == 2: self.update_color(2, self.calculate_color(x), self.back_color if self.choosen else self.front_color)
                elif i == 3: self.update_color(1, self.calculate_color(x), self.back_color if self.choosen else self.front_color)
                elif i == 4: self.update_color(0, self.calculate_color(x), self.back_color if self.choosen else self.front_color)
                
    def update_color(self, index, color, which):
        which[index] = which[index + 3] = which[index + 6] = which[index + 9] = color
        if which == self.front_color:
            self.front.remove()
            self.front = Rectangle(self.batch, *self.front_color_position, self.front_color, self.group)
        elif which == self.back_color:
            self.back.remove()
            self.back = Rectangle(self.batch, *self.back_color_position, self.back_color, self.group)
                
    def calculate_color(self, x):
        x = x - self.position[0]
        length = self.position[2] - self.position[0]
        return int((x*255/length))
        
    def update_position(self, x, y, x2, y2):
        self.position = [x, y, x2, y2]
        dx = x2 - (x2 - x)/8
        x2, dx = dx, x2
        dy = y2 - y
        self.front_color_position = [x2, y+dy/2, dx, y2]
        self.back_color_position = [x2, y, dx, y+dy/2]
        self.blue_position = [x, y, x2, y+dy/3]
        self.green_position = [x, y+dy/3, x2, y+dy*2/3]
        self.red_position = [x, y+dy*2/3, x2, y+dy]
        self.rectangles = [
            self.front_color_position,  # 0
            self.back_color_position,   # 1
            self.blue_position,         # 2
            self.green_position,        # 3
            self.red_position           # 4
        ]
            
    def get_front_color(self):
        return self.front_color[:3]
            
    def get_back_color(self):
        return self.back_color[:3]