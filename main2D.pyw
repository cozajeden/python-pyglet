from os import chdir
from os.path import realpath, dirname
chdir(realpath(dirname(__file__)))

from pyglet.gl import *
from pyglet.window import key, mouse, FPSDisplay
from threading import Timer
from model_object import Model
from toolbar_object import Toolbar
        

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Model()
        pyglet.clock.schedule(self.update)
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 30
        self.temp = None
        self.temp_index = None
        self.multitemp = None
        self.double_click_timer = None
        self.keys_pressed = set()
        self.opt = 0
        self.tools = {0: 'Line', 1: 'Rectangle', 2: 'Pixel', 3: 'Pixels', 4: 'Spray', 5: 'Polylines', 6: 'Polygon', 7: 'Circle'}
        self.opt_max = len(self.tools)
        self.group_number = 0
        self.group_object = pyglet.graphics.OrderedGroup(self.group_number)
        self.label = None
        self.show_tool()
        self.draw_area = [0, 0, self.width, 0.9*self.height]
        self.toolbar = Toolbar(self.model.batch, 0, self.draw_area[3], self.width/4, self.height)
        
    def group(self):
        self.group_number += 1
        self.group_object = pyglet.graphics.OrderedGroup(self.group_number)
        return self.group_object
        
    def show_tool(self):
        if self.label:
            self.label.begin_update()
            self.label.text = self.tools[self.opt]
            self.label.end_update()
        else:
            self.label = pyglet.text.Label(
                self.tools[self.opt],
                font_name='Times New Roman',
                font_size=36,
                x=self.width//2,
                y=self.height-36,
                anchor_x='center',
                anchor_y='center',
                batch = self.model.batch
            )
            
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
                if   self.opt == 0: self.temp = self.model.add_line(x=x, y=y, color=back_color+front_color, group=self.group())
                elif self.opt == 1: self.temp = self.model.add_rectangle(x=x, y=y, color=front_color+back_color+front_color+back_color, group=self.group())
                elif self.opt == 2: self.temp = self.model.add_pixels(position=[x, y], color=front_color, group=self.group())
                elif self.opt == 3: self.temp = self.model.add_pixels(position=[x, y], color=front_color, group=self.group())
                elif self.opt == 4: self.temp = self.model.add_spray(position=[x, y], intensity=100, radius=30, color=front_color, group=self.group())
                elif self.opt == 7: self.temp = self.model.add_circle(position=[x, y], radius=10, color=back_color+front_color, group=self.group())
                elif self.opt in (5, 6):
                    if not self.multitemp:
                        self.temp = self.model.add_line(x=x, y=y, color=back_color+front_color)
                        self.temp_index = self.model.get_last_index()
                    else:
                        self.multitemp.extend([x, y], front_color)
            elif (self.toolbar.position[0] < x < self.toolbar.position[2]) and (self.toolbar.position[1] < y < self.toolbar.position[3]):
                self.toolbar.on_mouse_press(x, y)
        if button == mouse.RIGHT:
            if self.multitemp:
                if self.opt in (5, 6):
                    self.multitemp.extend(self.multitemp.position[-2:])
                    self.temp = None
                    self.multitemp = None
        self.on_double_click_start()
        
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        front_color = self.toolbar.get_front_color()
        back_color = self.toolbar.get_back_color()
        if buttons == mouse.LEFT:
            if (self.draw_area[0] < x < self.draw_area[2]) and (self.draw_area[1] < y < self.draw_area[3]):
                if self.temp:
                    if   self.opt == 0: self.temp.update(x2=x, y2=y)
                    elif self.opt == 1: self.temp.update(x2=x, y2=y)
                    elif self.opt == 2: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 3: self.temp.update(position=[x, y], color=front_color, add=True)
                    elif self.opt == 4: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 7: self.temp.update(on_circumference_point=[x, y])
                    elif self.opt in (5, 6):
                        if self.temp:
                            self.temp.update(x2=x, y2=y)
                if self.multitemp:
                    if self.opt in (5, 6): self.multitemp.extend([x, y], front_color, True)
            elif (self.toolbar.position[0] < x < self.toolbar.position[2]) and (self.toolbar.position[1] < y < self.toolbar.position[3]):
                self.toolbar.on_mouse_press(x, y)
            
    def on_mouse_release(self, x, y, button, modifiers):
        front_color = self.toolbar.get_front_color()
        back_color = self.toolbar.get_back_color()
        if button == mouse.LEFT:
            if (self.draw_area[0] < x < self.draw_area[2]) and (self.draw_area[1] < y < self.draw_area[3]):
                if self.temp:
                    if   self.opt == 0: self.temp.update(x2=x, y2=y)
                    elif self.opt == 1: self.temp.update(x2=x, y2=y)
                    elif self.opt == 2: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 3: self.temp.update(position=[x, y], color=front_color, add=True)
                    elif self.opt == 4: self.temp.update(position=[x, y], color=front_color)
                    elif self.opt == 7: self.temp.update(on_circumference_point=[x, y])
                    elif self.opt in (5, 6):
                        self.temp.update(x2=x, y2=y)
                        if self.opt == 5: self.multitemp = self.model.add_polyline(position=self.temp.position, color=self.temp.color, group=self.group())
                        if self.opt == 6: self.multitemp = self.model.add_polygon(position=self.temp.position, color=self.temp.color, group=self.group())
                        self.model.remove_by_index(self.temp_index)
                        self.temp_index = None
                    self.temp = None 
                if self.multitemp:
                    if self.opt in (5, 6): self.multitemp.extend([x, y], front_color, True)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.LCTRL:
            self.keys_pressed.add(symbol)
        else:
            if symbol == key.ESCAPE:
                self.close()
            elif symbol == key.SPACE:
                self.opt +=1
                if self.opt >= self.opt_max:
                    self.opt = 0
                self.show_tool()
                self.multitemp = None
                self.temp_index = None
                self.temp = None
            elif symbol == key.Z and key.LCTRL in self.keys_pressed:
                self.multitemp = None
                self.temp_index = None
                self.temp = None
                self.model.remove_last_draw()
                
    def on_key_release(self, symbol, modifiers):
        self.pressed_keys.discard(symbol)
            
    def update(self, dt):
        pass
    
    def on_draw(self):
        self.clear()
        self.model.draw()
        self.fps_display.draw()
        
if __name__ == "__main__":
    window = Window(fullscreen=True, resizable=True)
    pyglet.app.run()
    
