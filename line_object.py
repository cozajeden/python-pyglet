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
        
    def update(self, position, color=None):
        if position[0]: self.position[0] = position[0]
        if position[1]: self.position[1] = position[1]
        if position[2]: self.position[2] = position[2]
        if position[3]: self.position[3] = position[3]
        if color: self.color = color
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.draw()
        
    def hide(self):
        self.vertex.delete()
        
    def remove(self):
        self.vertex.delete()
        del self