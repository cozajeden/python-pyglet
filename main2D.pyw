from os import chdir
from os.path import realpath, dirname
working_directory = realpath(dirname(__file__))
chdir(working_directory)

from pyglet.gl import *
from pyglet.window import key, mouse, FPSDisplay
from threading import Timer
from model_object import Model
from toolbar_object import Toolbar
import datetime

from numpy import pi, sin, cos, sqrt, exp
from random import random
        

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.clock.schedule(self.update)
        self.model = Model()
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 30
        self.keys_pressed = set()
        self.combo = []
        self.combo_timer = None
        self.combo_symbol = None
        self.temp = None
        self.rose = None
        self.temp_index = None
        self.multitemp = None
        self.double_click_timer = None
        self.opt = 0
        self.group_number = 0
        self.tools = {0: 'Line', 1: 'Rectangle', 2: 'Pixel', 3: 'Pixels', 4: 'Spray', 5: 'Polylines', 6: 'Polygon', 7: 'Circle'}
        self.opt_max = len(self.tools)
        self.group_object = [pyglet.graphics.OrderedGroup(self.group_number)]
        self.draw_area = [0, 0, self.width, 0.9*self.height]
        self.toolbar = Toolbar(self.model.batch, 0, self.draw_area[3], self.width, self.height, working_directory, self, pyglet.graphics.OrderedGroup(9999))
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.pos = [0,0,0]
        self.size = (self.width, self.height)
        
    def make_rose(self, position=None, radius=None, step=0.01, a=5, k=0.06, color=[0,0,0, 150,0,0]):
        if not position:
            position = [(self.draw_area[2] - self.draw_area[0])/2, (self.draw_area[3] - self.draw_area[1])/2]
        if not radius:
            radius = min(position + [(self.draw_area[2] - position[0]), (self.draw_area[3] - position[1])])
        step = 2*pi*step
        angle = step
        points = []
        step_radius = 0
        ratio = 1
        random_factor = lambda x: x*k*2 - x*4*k*random()
        
        while(step_radius < radius):
            z = a*exp((k + 1j)*angle)
            new_ratio = (radius*1.2 - step_radius)/radius
            ratio = min((new_ratio, ratio))
            points.extend([z.imag*ratio + position[1] + random_factor(step_radius), z.real*ratio + position[0] + random_factor(step_radius)])
            angle += step*random()
            step_radius = sqrt((position[0]-points[-1])**2 + (position[1]-points[-2])**2)
            
        points = position + points[::-1]
        color = color[:3] + color[3:]*(int(len(points)/2) - 1)
        self.temp = self.model.add_polygon(position=points, color=color, group=self.group())
        
    def on_resize(self, width, height):
        dx, dy = width/self.size[0], height/self.size[1]
        dx -= 1
        dy -= 1
        self.model.move_draws(z=[dx, dy])
        self.toolbar.on_resize(z=[dx, dy])
        self.size = (width, height)
        super().on_resize(width, height)
        
    def group(self, index=0):
        self.group_number += 1
        self.group_object.append(pyglet.graphics.OrderedGroup(self.group_number))
        return self.group_object[-1]
        
    # def show_tool(self):
    #     self.label_position = [self.width//2, self.height-36]
    #     if self.label:
    #         self.label.begin_update()
    #         self.label.text = self.tools[self.opt]
    #         self.label.end_update()
    #     else:
    #         self.label = pyglet.text.Label(
    #             self.tools[self.opt],
    #             font_name='Times New Roman',
    #             font_size=36,
    #             x=self.width//2,
    #             y=self.height-36,
    #             anchor_x='center',
    #             anchor_y='center',
    #             batch = self.model.batch,
    #             group = pyglet.graphics.OrderedGroup(9999)
    #         )
            
    def on_double_click(self, x, y, button):
        if self.double_click_timer:
            pass
    
    def on_double_click_start(self):
        if self.double_click_timer:
            self.on_double_click_stop()
        else:
            self.double_click_timer = Timer(0.2, self.on_double_click_stop)
            self.double_click_timer.start()
    
    def on_double_click_stop(self):
        if self.double_click_timer:
            self.double_click_timer.cancel()
            self.double_click_timer = None
        
    def on_mouse_press(self, x, y, button, modifiers):
        front_color = self.toolbar.get_front_color()
        back_color = self.toolbar.get_back_color()
        if button == mouse.LEFT:
            if (self.draw_area[0] < x < self.draw_area[2]) and (self.draw_area[1] < y < self.draw_area[3]):
                if   self.opt == 0: self.temp = self.model.add_line(position=[x, y, None, None], color=back_color+front_color, group=self.group())
                elif self.opt == 1: self.temp = self.model.add_rectangle(position=[x, y, None, None], color=front_color+back_color+front_color+back_color, group=self.group())
                elif self.opt == 2: self.temp = self.model.add_pixels(position=[x, y], color=front_color, group=self.group())
                elif self.opt == 3: self.temp = self.model.add_pixels(position=[x, y], color=front_color, group=self.group())
                elif self.opt == 4: self.temp = self.model.add_spray(position=[x, y], intensity=100, radius=30, color=front_color, group=self.group())
                elif self.opt == 7: self.temp = self.model.add_circle(position=[x, y], radius=1, color=back_color+front_color, group=self.group())
                elif self.opt in (5, 6):
                    if not self.multitemp:
                        self.temp = self.model.add_line(position=[x, y, None, None], color=back_color+front_color)
                        self.temp_index = self.model.get_last_index()
                    else:
                        self.multitemp.extend([x, y], front_color)
        if button == mouse.RIGHT and self.draw_area[0] < x < self.draw_area[2] and self.draw_area[1] < y < self.draw_area[3]:
            if self.multitemp:
                if self.opt in (5, 6):
                    self.multitemp.extend(self.multitemp.position[-2:])
                    self.temp = None
                    self.multitemp = None
        self.on_double_click_start()
        self.toolbar.on_mouse_press(x, y, button)
        
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        front_color = self.toolbar.get_front_color()
        back_color = self.toolbar.get_back_color()
        if buttons == mouse.LEFT:
            if (self.draw_area[0] < x < self.draw_area[2]) and (self.draw_area[1] < y < self.draw_area[3]):
                if self.temp:
                    if   self.opt == 0: self.temp.update([None, None, x, y])
                    elif self.opt == 1: self.temp.update([None, None, x, y])
                    elif self.opt == 2: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 3: self.temp.update(position=[x, y], color=front_color, add=True)
                    elif self.opt == 4: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 7: self.temp.update(on_circumference_point=[x, y])
                    elif self.opt in (5, 6):
                        if self.temp:
                            self.temp.update([None, None, x, y])
                if self.multitemp:
                    if self.opt in (5, 6): self.multitemp.extend([x, y], front_color, True)
            elif (self.toolbar.position[0] < x < self.toolbar.position[2]) and (self.toolbar.position[1] < y < self.toolbar.position[3]):
                self.toolbar.on_mouse_press(x, y, buttons)
            
    def on_mouse_release(self, x, y, button, modifiers):
        front_color = self.toolbar.get_front_color()
        back_color = self.toolbar.get_back_color()
        if button == mouse.LEFT:
            if (self.draw_area[0] < x < self.draw_area[2]) and (self.draw_area[1] < y < self.draw_area[3]):
                if self.temp:
                    if   self.opt == 0: self.temp.update([None, None, x, y])
                    elif self.opt == 1: self.temp.update([None, None, x, y])
                    elif self.opt == 2: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 3: self.temp.update(position=[x, y], color=front_color, add=True)
                    elif self.opt == 4: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 7: self.temp.update(on_circumference_point=[x, y])
                    elif self.opt in (5, 6):
                        self.temp.update([None, None, x, y])
                        if self.opt == 5: self.multitemp = self.model.add_polyline(position=self.temp.position, color=self.temp.color, group=self.group())
                        if self.opt == 6: self.multitemp = self.model.add_polygon(position=self.temp.position, color=self.temp.color, group=self.group())
                        self.model.remove_by_index(self.temp_index)
                        self.temp_index = None
                    self.temp = None 
                if self.multitemp:
                    if self.opt in (5, 6): self.multitemp.extend([x, y], front_color, True)
        
    def start_combo(self, symbol):
        if self.combo_timer:
            self.combo_timer.cancel()
            self.combo_timer = None
        if symbol == key.E and self.combo == [key.R, key.O, key.S]:
            self.make_rose()
            self.combo = []
        elif symbol == key.S and self.combo == [key.R, key.O]:
            self.combo.append(symbol)
            self.combo_timer = Timer(0.5, self.stop_combo); self.combo_timer.start()
        elif symbol == key.O and self.combo == [key.R]:
            self.combo.append(symbol)
            self.combo_timer = Timer(0.5, self.stop_combo); self.combo_timer.start()
        elif symbol == key.R:
            self.combo = [symbol]
            self.combo_timer = Timer(0.5, self.stop_combo); self.combo_timer.start()
    
    def stop_combo(self):
        if self.combo_timer:
            self.combo_timer.cancel()
            self.combo_timer = None
            self.combo = []
        
    def on_key_press(self, symbol, modifiers):
        self.keys_pressed.add(symbol)
        self.start_combo(symbol)
        if symbol == key.LCTRL:
            pass
        else:
            if symbol == key.F10: pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot' + datetime.datetime.now().strftime("%m_%d_%Y-%H_%M_%S_%ms") + '.png')
            if symbol == key.ESCAPE: self.close()
            elif key.LCTRL in self.keys_pressed:
                if symbol == key.Z:
                    self.multitemp = None
                    self.temp_index = None
                    self.temp = None
                    self.model.remove_last_draw()
                if symbol == key.S:
                    self.model.save('save.txt')
                if symbol == key.L:
                    self.model.load('save.txt')
                
    def on_key_release(self, symbol, modifiers):
        self.pressed_keys.discard(symbol)
            
    def update(self, dt):
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        self.push(dt)
        
    def push(self, dt):
        x, y, z = 0, 0, 0
        if self.keys[key.E]: z = dt
        if self.keys[key.Q]: z = -dt
        dt = dt*70
        if self.keys[key.W]: y = dt
        if self.keys[key.S]: y = -dt
        if self.keys[key.A]: x = -dt
        if self.keys[key.D]: x = dt
        self.model.move_draws(x, y, z, origin=[self._mouse_x, self._mouse_y])
    
    def on_draw(self):
        self.clear()
        self.model.draw()
        self.fps_display.draw()
        
if __name__ == "__main__":
    window = Window(fullscreen=True, resizable=True)
    pyglet.app.run()
    
