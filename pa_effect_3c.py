from math import sin, cos
from pa_effect import paCEffect
from jtruk_3d import jtruk3DSetGfx, makeV, jtruk3DModelBoxLines, jtruk3DModelIcosahedron

# box=jtruk3DModelBoxLines()

class paCEffect3C(paCEffect):
    def __init__(self, iVersion):
        super().__init__()

        self.icosahedron=jtruk3DModelIcosahedron()

        self.x, self.y, self.z = 0, -1, 0
        self.dx, self.dy, self.dz = .07, .01, .12
        self.rx, self.rz = 0, 0        
        self.drx, self.drz = .07, .07
        self.vertices = []
        self.triangles = []
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        rX,rY,rZ = lerpPos*19,self.rx, self.rz
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        overY = self.y - 1
        if overY > 0:
            self.y = 1 - (self.dy-overY)
            self.dy = -self.dy
        if self.x < -3 or self.x > 3:
            self.dx = -self.dx
            self.drz = -self.drz
        if self.z < -1 or self.z > 1:
            self.dz = -self.dz
            self.drx = -self.drx
        self.dy += .02
        self.rx += self.drx
        self.rz += self.drz
        self.icosahedron.draw(gfx, display, [rX, rY, rZ], [self.x, self.y, 5+self.z], None, lerpPos)

    def legend(self):
        return "Icosahedron"
    
    def detail(self):
        return "With basic face lighting"
