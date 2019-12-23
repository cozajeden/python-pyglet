from pyglet.gl import *

class Line:
    def __init__(self, batch, x, y, x2=None, y2=None, color=[255]*6):
        self.position = [x, y, x2, y2]
        self.color = color
        self.batch = batch
        self.vertex = None
        try:
            if x2 and y2: self.draw()
            elif not x2 and not y2: pass
            else: raise AttributeError
        except AttributeError:
            exit(f"""Program ends with AttributeError for object={self}:
    Line(batch={batch}, x={x}, y={y}, x2={x2}, y2={y2}, color={color})
    Possible calls:
    Line(batch, x, y)
    Line(batch, x, y, x2, y2)
    color - optional, otherwise white-white""")
        
    def draw(self):
        self.vertex = self.batch.add(2, GL_LINES, None,
                                ('v2f', self.position), 
                                ('c3B', self.color))
        
    def update(self, x=None, y=None, x2=None, y2=None, color=None):
        if x: self.position[0] = x
        if y: self.position[1] = y
        if x2: self.position[2] = x2
        if y2: self.position[3] = y2
        if color: self.color = color
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.draw()
        
    def remove(self):
        self.vertex.delete()