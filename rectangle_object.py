from pyglet.gl import *

class Rectangle:
    def __init__(self, batch, position, color=None, group=None):
        if not color:
            color=[255]*12
        self.group = group
        if len(position) == 8:
            self.position = position
        else:
            self.position = [position[0], position[1], position[2], position[1], position[2], position[3], position[0], position[3]]
        self.color = color
        self.batch = batch
        self.vertex = None
        try:
            if position[2] and position[3]: self.draw()
            elif not position[2] and not position[3]: pass
            else: raise AttributeError
        except AttributeError:
            exit(f"""Program ends with AttributeError for object={self}:
    Rectangle(batch={batch}, x={x}, y={y}, x2={x2}, y2={y2}, color={color})
    Possible calls:
    Rectangle(batch, x, y)
    Rectangle(batch, x, y, x2, y2)
    color - optional, otherwise white-white-white-white""")
    
    def draw(self):
        self.vertex = self.batch.add(4, GL_QUADS, self.group,
                                ('v2f', self.position), 
                                ('c3B', self.color))
        
    def update(self, position, color=None):
        if position[0]: self.position[0], self.position[6] = position[0], position[0]
        if position[1]: self.position[1], self.position[3] = position[1], position[1]
        if position[2]: self.position[2], self.position[4] = position[2], position[2]
        if position[3]: self.position[5], self.position[7] = position[3], position[3]
        if color: self.color = color
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.draw()
        
    def remove(self):
        self.vertex.delete()
        del self
        
    def hide(self):
        self.vertex.delete()