from pyglet.gl import *
from pyglet.window import mouse
from rectangle_object import Rectangle
from polyline_object import Polyline
from line_object import Line
from sprite_object import Sprite
from os.path import join

class Toolbar:
    def __init__(self, batch, x, y, x2, y2, directory, window, group=None):
        self.window = window
        self.group = group
        self.batch = batch
        self.tools = {0: 'Line', 1: 'Rectangle', 2: 'Pixel', 3: 'Pixels', 4: 'Spray', 5: 'Polylines', 6: 'Polygon', 7: 'Circle', 8: 'Sprite'}
        self.update_position(x, y, x2, y2)
        self.blue_color =  [0]*5 + [255] + [0]*2 + [255] + [0]*3
        self.green_color = [0]*4 + [255] + [0]*2 + [255] + [0]*4
        self.red_color =   [0]*3 + [255] + [0]*2 + [255] + [0]*5
        self.front_color = [255]*12
        self.back_color =  [0]*12
        self.choosen =     0
        self.main_color =  0
        self.blue =        Rectangle(self.batch, self.blue_position, self.blue_color, self.group)
        self.green =       Rectangle(self.batch, self.green_position, self.green_color, self.group)
        self.red =         Rectangle(self.batch, self.red_position, self.red_color, self.group)
        self.front =       Rectangle(self.batch, self.front_color_position, self.front_color, self.group)
        self.back =        Rectangle(self.batch, self.back_color_position, self.back_color, self.group)
        self.which_color = Polyline(self.batch, self.which_color_outline[0], [255,0,255]*8, self.group )
        self.blue_line =  Line(self.batch, self.blue_line_position, [100,100,100]*2, self.group)
        self.green_line = Line(self.batch, self.green_line_position, [100,100,100]*2, self.group)
        self.red_line =   Line(self.batch, self.red_line_position, [100,100,100]*2, self.group)
        self.line_sprite_path =      [join(directory, 'sprites', 'pressed_line.png'), join(directory, 'sprites', 'unpressed_line.png')]
        self.rectangle_sprite_path = [join(directory, 'sprites', 'pressed_rectangle.png'), join(directory, 'sprites', 'unpressed_rectangle.png')]
        self.pixel_sprite_path =     [join(directory, 'sprites', 'pressed_pixel.png'), join(directory, 'sprites', 'unpressed_pixel.png')]
        self.pixels_sprite_path =    [join(directory, 'sprites', 'pressed_pixels.png'), join(directory, 'sprites', 'unpressed_pixels.png')]
        self.spray_sprite_path =     [join(directory, 'sprites', 'pressed_spray.png'), join(directory, 'sprites', 'unpressed_spray.png')]
        self.polyline_sprite_path =  [join(directory, 'sprites', 'pressed_polyline.png'), join(directory, 'sprites', 'unpressed_polyline.png')]
        self.polygon_sprite_path =   [join(directory, 'sprites', 'pressed_polygon.png'), join(directory, 'sprites', 'unpressed_polygon.png')]
        self.circle_sprite_path =    [join(directory, 'sprites', 'pressed_circle.png'), join(directory, 'sprites', 'unpressed_circle.png')]
        self.sprites_paths = [
        self.line_sprite_path, self.rectangle_sprite_path, self.pixel_sprite_path, self.pixels_sprite_path,
        self.spray_sprite_path, self.polyline_sprite_path, self.polygon_sprite_path, self.circle_sprite_path
        ]
        self.line_sprite_object =      Sprite(self.batch, self.line_sprite_position, self.line_sprite_path[0], self.group)
        self.rectangle_sprite_object = Sprite(self.batch, self.rectangle_sprite_position, self.rectangle_sprite_path[1], self.group)
        self.pixel_sprite_object =     Sprite(self.batch, self.pixel_sprite_position, self.pixel_sprite_path[1], self.group)
        self.pixels_sprite_object =    Sprite(self.batch, self.pixels_sprite_position, self.pixels_sprite_path[1], self.group)
        self.spray_sprite_object =     Sprite(self.batch, self.spray_sprite_position, self.spray_sprite_path[1], self.group)
        self.polyline_sprite_object =  Sprite(self.batch, self.polyline_sprite_position, self.polyline_sprite_path[1], self.group)
        self.polygon_sprite_object =   Sprite(self.batch, self.polygon_sprite_position, self.polygon_sprite_path[1], self.group)
        self.circle_sprite_object =    Sprite(self.batch, self.circle_sprite_position, self.circle_sprite_path[1], self.group)
        self.draws = [
            self.blue, self.green, self.red, self.front, self.back,
            self.which_color, self.blue_line, self.green_line, self.red_line,
            self.line_sprite_object, self.rectangle_sprite_object,
            self.pixel_sprite_object, self.pixels_sprite_object,
            self.spray_sprite_object, self.polyline_sprite_object,
            self.polygon_sprite_object, self.circle_sprite_object
        ]
        
    def on_mouse_press(self, x, y, button):
        for i, r in enumerate(self.rectangles):
            if (r[0] < x < r[2]) and (r[1] < y < r[3]):
                if button == mouse.LEFT:
                    if i in range(5,13):
                        self.draws[self.window.opt + 9].path = self.sprites_paths[self.window.opt][1]
                        self.window.multitemp = None
                        self.window.temp_index = None
                        self.window.temp = None
                    if   i == 0:  self.choosen = 0; self.update_color_lines(self.front)
                    elif i == 1:  self.choosen = 1; self.update_color_lines(self.back)
                    elif i == 2:  self.update_color(2, x, self.back_color if self.choosen else self.front_color)
                    elif i == 3:  self.update_color(1, x, self.back_color if self.choosen else self.front_color)
                    elif i == 4:  self.update_color(0, x, self.back_color if self.choosen else self.front_color)
                    elif i in range(5,13):
                        self.window.opt = i - 5;
                        self.draws[i + 4].path = self.sprites_paths[i - 5][0]
                        for each in self.draws[9:17]:
                            each.hide()
                            each.draw()
                if button == mouse.RIGHT:
                    if   i == 0 and self.main_color == 1:
                        self.front_color, self.back_color, self.main_color = self.back_color,  self.front_color, 0
                        self.which_color.position =  self.which_color_outline[0]
                        self.which_color.hide(); self.which_color.draw()
                    if   i == 1 and self.main_color == 0:
                        self.front_color, self.back_color, self.main_color = self.back_color,  self.front_color, 1
                        self.which_color.position =  self.which_color_outline[1]
                        self.which_color.hide(); self.which_color.draw()
                        
    def on_resize(self, z, origin=[0,0]):
        for each in self.draws:
            each.position = list(map(lambda n: (n[1]-origin[0])*(1 + z[0])+origin[0] if not n[0]%2 else n[1], enumerate(each.position)))
            each.position = list(map(lambda n: (n[1]-origin[1])*(1 + z[1])+origin[1] if n[0]%2 else n[1], enumerate(each.position)))
            each.hide(); each.draw()
        self.update_position(self.position[0]*(1 + z[0]), self.position[1]*(1 + z[1]),
                             self.position[2]*(1 + z[0]), self.position[3]*(1 + z[1]))
                        
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
            self.front.hide()
            self.front.color =  self.front_color
            self.front.draw()
        elif which == self.back_color:
            self.back.hide()
            self.back.color = self.back_color
            self.back.draw()
        if index == 0:
            self.red_line.position[0], self.red_line.position[2] = x, x
        elif index == 1:
            self.green_line.position[0], self.green_line.position[2] = x, x
        elif index == 2:
            self.blue_line.position[0], self.blue_line.position[2] = x, x
        self.red_line.hide(); self.red_line.draw()
        self.green_line.hide(); self.green_line.draw()
        self.blue_line.hide(); self.blue_line.draw()
                
    def calculate_color(self, x):
        x = x - self.blue.position[0]
        length = self.blue.position[2] - self.blue.position[0]
        return int((x*255/length))
        
    def update_position(self, x, y, x2, y2):
        self.position = [x, y, x2, y2]
        sx, sy, sx2, sy2 = x2/4, y, x2, y2
        dx, dy = (sx2 - sx)/4, (sy2 - sy)/2
        dx, dy = min(dx, dy), min(dx, dy)
        self.line_sprite_position = [sx,sy, sx+dx,sy+dy]
        self.rectangle_sprite_position = [sx,sy+dy, sx+dx,sy+dy*2]
        self.pixel_sprite_position = [sx+dx,sy, sx+dx*2,sy+dy]
        self.pixels_sprite_position = [sx+dx,sy+dy, sx+dx*2,sy+dy*2]
        self.spray_sprite_position = [sx+dx*2,sy, sx+dx*3,sy+dy]
        self.polyline_sprite_position = [sx+dx*2,sy+dy, sx+dx*3,sy+dy*2]
        self.polygon_sprite_position = [sx+dx*3,sy, sx+dx*4,sy+dy]
        self.circle_sprite_position = [sx+dx*3,sy+dy, sx+dx*4,sy+dy*2]
        x2 = sx
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
            self.front_color_position,      # 0
            self.back_color_position,       # 1
            self.blue_position,             # 2
            self.green_position,            # 3
            self.red_position,              # 4
            self.line_sprite_position,       # 5
            self.rectangle_sprite_position,  # 6
            self.pixel_sprite_position,      # 7
            self.pixels_sprite_position,     # 8
            self.spray_sprite_position,      # 9
            self.polyline_sprite_position,   # 10    
            self.polygon_sprite_position,    # 11
            self.circle_sprite_position      # 12
        ]
            
    def get_front_color(self):
        return self.front_color[:3]
            
    def get_back_color(self):
        return self.back_color[:3]