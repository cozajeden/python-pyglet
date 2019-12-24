from pyglet.gl import *

class Pixels:
    def __init__(self, batch, position, color=None):
        self.position = position
        self.length = int(len(position)/2)
        if not color:
            color = [255]*3*self.length
        self.color = color
        self.batch = batch
        self.vertex = None
        try:
            if position: self.draw()
            else: raise AttributeError
        except AttributeError:
            exit(f"""Program ends with AttributeError for object={self}:
    Pixels(batch={batch}, position={position}, color={color})
    Possible calls:
    Pixels(batch, position)
    color - optional, otherwise white-white""")
        
    def draw(self):
        self.vertex = self.batch.add(self.length, GL_POINTS, None,
                                ('v2f', self.position), 
                                ('c3B', self.color))
        
    def update(self, points=None, position=None, color=None, add=False):
        if points and not position:
            if color: self.color = color
        elif position:
            if add:
                self.length += int(len(position)/2)
                self.position += position
                if color: self.color += color
                else: self.color += [255]*3*int(len(position)/2)
            else:
                self.length = int(len(position)/2)
                self.position = position
                if color: self.color = color
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.draw()
        
    def remove(self):
        self.vertex.delete()
        del self