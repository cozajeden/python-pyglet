from pyglet.gl import *
from pyglet.window import key, FPSDisplay
from numpy import pi, cos, sin
from functools import lru_cache

import pyglet.gl as p


class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, x=0, y=0, z=-1):

        self.top = self.get_tex(r'C:\Users\rnapier\Downloads\Basic Pyglet Cube\Basic Pyglet Cube\grass_top.png')
        self.side = self.get_tex(r'C:\Users\rnapier\Downloads\Basic Pyglet Cube\Basic Pyglet Cube\grass_side.png')
        self.bottom = self.get_tex(r'C:\Users\rnapier\Downloads\Basic Pyglet Cube\Basic Pyglet Cube\dirt.png')
        
        self.batch = pyglet.graphics.Batch()
        self.add_to_batch(x, y, z)

    def add_to_batch(self, x=0, y=0, z=-1):
        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1, ))

        #x,y,z = 0,0,-1
        X,Y,Z = x+1,y+1,z+1

        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.bottom,('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.top,('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),tex_coords)

    def draw(self):
        self.batch.draw()



class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90: self.rot[0] = 90
        elif self.rot[0]<-90: self.rot[0] = -90

    def update(self,dt,keys):
        s = dt*10
        rotY = -self.rot[1]/180*pi
        dx,dz = s*sin(rotY),s*cos(rotY)
        if keys[key.W]: self.pos[0]+=dx; self.pos[2]-=dz
        if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
        if keys[key.A]: self.pos[0]-=dz; self.pos[2]-=dx
        if keys[key.D]: self.pos[0]+=dz; self.pos[2]+=dx

        if keys[key.SPACE]: self.pos[1]+=s
        if keys[key.LSHIFT]: self.pos[1]-=s


class Window(pyglet.window.Window):

    def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2],)
    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
    def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    def set2d(self): self.Projection(); gluOrtho2D(0,self.width,0,self.height); self.Model()
    def set3d(self): self.Projection(); gluPerspective(70,self.width/self.height,0.05,1000); self.Model()

    def setLock(self,state): self.lock = state; self.set_exclusive_mouse(state)
    lock = False; mouse_lock = property(lambda self:self.lock,setLock)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 30

        self.model = Model()
        
        self.models_count = (-0, 200, -0, 200)
        
        for x in range(self.models_count[0], self.models_count[1]):
             for z in range(self.models_count[2], self.models_count[3]):
                 self.model.add_to_batch(x, 0, -z-1)
        self.player = Player((0.5,1.5,1.5),(-30,0))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock
        elif KEY == key.F10 : pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

    def update(self,dt):
        self.player.update(dt,self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        self.fps_display.draw()
        glPopMatrix()

if __name__ == '__main__':
    window = Window(caption='Minecraft',resizable=True, vsync=True, fullscreen=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    pyglet.app.run()



