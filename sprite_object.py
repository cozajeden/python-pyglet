from pyglet.gl import *

class Sprite:
    def __init__(self, batch, position, path, group=None):
        self.path = path
        self.group = group
        if len(position) == 8:
            self.position = position
        else:
            self.position = [position[0], position[1], position[2], position[1], position[2], position[3], position[0], position[3]]
        self.batch = batch
        self.vertex = None
        try:
            if position[2] and position[3]: self.draw()
            elif not position[2] and not position[3]: pass
            else: raise AttributeError
        except AttributeError:
            exit(f"""Program ends with AttributeError for object={self}:
    Sprite(batch={batch}, position={position}, path={path})
    Possible calls:
    Sprite(batch, position, path)""")
            
    def get_texture(self):
        tex = pyglet.image.load(self.path).get_texture()
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        self.texure = pyglet.graphics.TextureGroup(tex)
    
    def draw(self):
        self.get_texture()
        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1, ))
        self.vertex = self.batch.add(4, GL_QUADS, self.texure, ('v2f',self.position), tex_coords)
        
    def update(self, x=None, y=None, x2=None, y2=None, path=None):
        if x: self.position[0], self.position[6] = x, x
        if y: self.position[1], self.position[3] = y, y
        if x2: self.position[2], self.position[4] = x2, x2
        if y2: self.position[5], self.position[7] = y2, y2
        if path: self.path = path
        if self.vertex:
            self.vertex.delete()
            self.vertex = None
        self.draw()
        
    def remove(self):
        self.vertex.delete()
        del self
        
    def hide(self):
        self.vertex.delete()