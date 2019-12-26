from pyglet.gl import *
from pyglet.window import mouse
from rectangle_object import Rectangle
from polyline_object import Polyline
from line_object import Line

class Toolbar:
    def __init__(self, batch, x, y, x2, y2, group=None):
        self.group = group
        self.batch = batch
        self.tools = {0: 'Line', 1: 'Rectangle', 2: 'Pixel', 3: 'Pixels', 4: 'Spray', 5: 'Polylines', 6: 'Polygon', 7: 'Circle'}
        self.update_position(x, y, x2, y2)
        self.blue_color = [0]*5 + [255] + [0]*2 + [255] + [0]*3
        self.green_color = [0]*4 + [255] + [0]*2 + [255] + [0]*4
        self.red_color = [0]*3 + [255] + [0]*2 + [255] + [0]*5
        self.front_color = [255]*12
        self.back_color = [0]*12
        self.choosen = 0
        self.main_color = 0
        self.blue = Rectangle(self.batch, self.blue_position, self.blue_color, self.group)
        self.green = Rectangle(self.batch, self.green_position, self.green_color, self.group)
        self.red = Rectangle(self.batch, self.red_position, self.red_color, self.group)
        self.front = Rectangle(self.batch, self.front_color_position, self.front_color, self.group)
        self.back = Rectangle(self.batch, self.back_color_position, self.back_color, self.group)
        self.which_color = Polyline(self.batch, self.which_color_outline[0], [255,0,255]*8, self.group )
        self.blue_line = Line(self.batch, self.blue_line_position, [100,100,100]*2, self.group)
        self.green_line = Line(self.batch, self.green_line_position, [100,100,100]*2, self.group)
        self.red_line = Line(self.batch, self.red_line_position, [100,100,100]*2, self.group)
        
    def on_mouse_press(self, x, y, button):
        for i, r in enumerate(self.rectangles):
            if (r[0] < x < r[2]) and (r[1] < y < r[3]):
                if button == mouse.LEFT:
                    if   i == 0: self.choosen = 0; self.update_color_lines(self.front)
                    elif i == 1: self.choosen = 1; self.update_color_lines(self.back)
                    elif i == 2: self.update_color(2, x, self.back_color if self.choosen else self.front_color)
                    elif i == 3: self.update_color(1, x, self.back_color if self.choosen else self.front_color)
                    elif i == 4: self.update_color(0, x, self.back_color if self.choosen else self.front_color)
                if button == mouse.RIGHT:
                    if   i == 0 and self.main_color == 1:
                        self.front_color, self.back_color, self.main_color = self.back_color,  self.front_color, 0
                        self.which_color.position =  self.which_color_outline[0]
                        self.which_color.hide(); self.which_color.draw()
                    if   i == 1 and self.main_color == 0:
                        self.front_color, self.back_color, self.main_color = self.back_color,  self.front_color, 1
                        self.which_color.position =  self.which_color_outline[1]
                        self.which_color.hide(); self.which_color.draw()
                        
    def update_color_lines(self, color):
        self.blue_line.position[0] = color.color[2]*(self.blue.position[2] - self.blue.position[0])/255 + self.blue.position[0]
        self.blue_line.position[2] = self.blue_line.position[0]
        self.green_line.position[0] = color.color[1]*(self.green.position[2] - self.green.position[0])/255 + self.green.position[0]
        self.green_line.position[2] = self.green_line.position[0]
        self.red_line.position[0] = color.color[0]*(self.red.position[2] - self.red.position[0])/255 + self.red.position[0]
        self.red_line.position[2] = self.red_line.position[0] 
        self.red_line.hide(); self.red_line.draw()
        self.green_line.hide(); self.green_line.draw()
        self.blue_line.hide(); self.blue_line.draw()
                
    def update_color(self, index, x, which):
        """index - 0: 'red', 1: 'green', 2: 'blue'"""
        which[index] = which[index + 3] = which[index + 6] = which[index + 9] = self.calculate_color(x)
        if which == self.front_color:
            self.front.remove()
            self.front = Rectangle(self.batch, self.front_color_position, self.front_color, self.group)
        elif which == self.back_color:
            self.back.remove()
            self.back = Rectangle(self.batch, self.back_color_position, self.back_color, self.group)
        if index == 0:
            self.red_line_position[0], self.red_line_position[2] = x, x
        elif index == 1:
            self.green_line_position[0], self.green_line_position[2] = x, x
        elif index == 2:
            self.blue_line_position[0], self.blue_line_position[2] = x, x
        self.red_line.hide(); self.red_line.draw()
        self.green_line.hide(); self.green_line.draw()
        self.blue_line.hide(); self.blue_line.draw()
                
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
        self.blue_line_position = [self.blue_position[2], self.blue_position[1], self.blue_position[2], self.blue_position[3]]
        self.red_line_position = [self.red_position[2], self.red_position[1], self.red_position[2], self.red_position[3]]
        self.green_line_position = [self.green_position[2], self.green_position[1], self.green_position[2], self.green_position[3]]
        self.which_color_outline = [[
            self.front_color_position[0], self.front_color_position[1], self.front_color_position[2], self.front_color_position[1],
            self.front_color_position[2], self.front_color_position[1], self.front_color_position[2], self.front_color_position[3],
            self.front_color_position[2], self.front_color_position[3], self.front_color_position[0], self.front_color_position[3],
            self.front_color_position[0], self.front_color_position[3], self.front_color_position[0], self.front_color_position[1]],[
            self.back_color_position[0], self.back_color_position[1], self.back_color_position[2], self.back_color_position[1],
            self.back_color_position[2], self.back_color_position[1], self.back_color_position[2], self.back_color_position[3],
            self.back_color_position[2], self.back_color_position[3], self.back_color_position[0], self.back_color_position[3],
            self.back_color_position[0], self.back_color_position[3], self.back_color_position[0], self.back_color_position[1]
            ]]
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