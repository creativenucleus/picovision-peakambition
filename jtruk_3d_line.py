from jtruk_3d import jtruk3DModel, makeV
from random import random

class jtruk3DModelLine(jtruk3DModel):
    def __init__(self, nPoints, hueU, z):
        super().__init__()
        
        self.hueU = hueU
        for i in range(nPoints):
            x = (i/(nPoints - 1))*2 - 1 # -1 to 1
            y = random()*2 - 1	# -1 to 1
            self.appendVerts([makeV(x,y,z)])
        
    def _draw(self, gfx, verts, T, extra):
        gfx.set_pen(gfx.create_pen_hsv(self.hueU, 1, 1))

        for i in range(1, len(verts)):
            gfx.line(verts[i-1]['pp'][0],verts[i-1]['pp'][1], verts[i]['pp'][0], verts[i]['pp'][1])
