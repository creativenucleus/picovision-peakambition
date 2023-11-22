# Source from Peak Ambition (jtruk)
# License: Pirate's Honour
# You're welcome to take / copy / adapt, but please:
# 1) Drop me a little credit if you do, thanks :)
# 2) Leave this header in place, to retain the license info.
# 3) Let me know if you use / improve it!
# Full source: https://github.com/creativenucleus/picovision-peakambition/

from pa_effect import paCEffect
from jtruk_3d_platonic_solid import jtruk3DPlatonicSolid

class paCEffect3C(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        self.iVersion = iVersion

        self.icosahedron=jtruk3DPlatonicSolid(1)

        self.x, self.y, self.z = 0, -1, 0
        self.dx, self.dy, self.dz = .15, .01, .09
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
        self.icosahedron.draw(gfx, display, [rX, rY, rZ], [self.x, self.y, self.z + 5], None, extra={'pulse': self.iVersion == 1})

    def legend(self):
        return "Flat Polygons"
    
    def detail(self):
        return "The icosahedron is a solid with 20 faces.\nIt's neatly defined by three overlapping boxes\nThere's some normal and dot-product maths to do nice face\nlighting"
