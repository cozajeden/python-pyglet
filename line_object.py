from pyglet.gl import *

class Line:
    def __init__(self, batch, position, color=None, group=None):
        if not color:
            color = [255]*6
        self.group = group
        self.position = position
        self.color = color
        self.batch = batch
        self.vertex = None
        try:
            if position[2] and position[3]: self.draw()
            elif not position[2] and not position[3]: pass
            else: raise AttributeError
        except AttributeError:
            exit(f"""Program ends with AttributeError for object={self}:
    Line(batch={batch}, position={position}, color={color})
    Possible calls:
    Line(batch, position)
    color - optional, otherwise white-white""")
        
    def draw(self):
        self.vertex = self.batch.add(2, GL_LINES, self.group,
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
        del self