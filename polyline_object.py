from pyglet.gl import *

class Polyline:
    def __init__(self, batch, position, color=None):
        self.position = position
        if not color:
            color = [255]*int(len(position)/2)
        self.color = color
        self.batch = batch
        self.vertex = None
        try:
            if position: self.draw()
            else: raise AttributeError
        except AttributeError:
            exit(f"""Program ends with AttributeError for object={self}:
    Polyline(batch={batch}, position={position}, color={color})
    Possible calls:
    Polyline(batch, position)
    color - optional, otherwise white-white""")
        
    def draw(self):
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.vertex = self.batch.add(int(len(self.position)/2), GL_LINES, None,
                                ('v2f', self.position), 
                                ('c3B', self.color))
        
    def hide(self):
        self.vertex.delete()
        self.vertex = None
        
    def update(self, position=None, color=None, add=False):
        if not color:
            color = [255]*3*int(len(position)/2)
        if add:
            if position: self.position += position
            if color: self.color = +color
        else:
            if position: self.position = position
            if color: self.color = color
        self.draw()
        
    def extend(self, position, color=[255]*3, update=False):
        print(update)
        if not update:
            if len(color) == 3:
                self.color += self.color[-3:] + color
            elif len(color) == 6:
                self.color += color
            self.position.extend(self.position[-2:] + position)
        else:
            print(position)
            self.position = self.position[:-2] + position
        self.draw()
        
    def remove(self):
        self.vertex.delete()
        del self