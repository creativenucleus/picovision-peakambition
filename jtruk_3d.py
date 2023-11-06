from math import floor, sin, cos, pi

GFX=None

def jtruk3DSetGfx(gfx):
    global GFX
    GFX=gfx

class jtruk3DModel:
    def __init__(self):
        self.verts = []
    
    # [[x, y, z], [x, y, z]...]
    def appendVerts(self, verts):
        self.verts.extend(verts)
    
    # display: {w}
    # trans: None or {x,y,z}
    # rot: None or {x,y,z}
    def draw(self, display, rotL, trans, rotW):
        verts = []
        for v in self.verts:
            x, y, z = v[0], v[1], v[2]

            # Rotate (optional)
            a=105
            if rotL != None:
                if rotL[0] != 0:
                    sina,cosa=sin(rotL[0]),cos(rotL[0])
                    y, z = y*cosa-z*sina, y*sina+z*cosa 
                if rotL[1] != 0:
                    sina,cosa=sin(rotL[1]),cos(rotL[1])
                    x, z = x*cosa-z*sina, x*sina+z*cosa
                if rotL[2] != 0:
                    sina,cosa=sin(rotL[2]),cos(rotL[2])
                    x, y = x*cosa-y*sina, x*sina+y*cosa

            # Translate (optional)
            if trans != None:
                x, y, z = x+trans[0], y+trans[1], z+trans[2]
            
            # Rotate (optional)
            if rotW != None:
                if rotW[0] != 0:
                    sina,cosa=sin(rotW[0]), cos(rotW[0]),
                    y, z = y*cosa-z*sina, y*sina+z*cosa 
                if rotW[1] != 0:
                    sina,cosa=sin(rotW[1]), cos(rotW[1]),
                    x, z = x*cosa-z*sina, x*sina+z*cosa
                if rotW[2] != 0:
                    sina,cosa=sin(rotW[2]), cos(rotW[2]),
                    x, y = x*cosa-y*sina, x*sina+y*cosa
                                
            zF=7-z/1.5
            verts.append([
                floor(display['xmid']+(x/zF)*display['scale']),
                floor(display['ymid']+(y/zF)*display['scale']),
                z/zF
            ])

        # Draw
        self._draw(verts)

    def _draw(self, verts):
        raise Exception("There must be a _draw function for this class")


class jtruk3DModelBoxLines(jtruk3DModel):
    def __init__(self):
        super().__init__() 

        self.appendVerts([[-1,-1,-1], [-1,-1,1], [-1,1,-1], [-1,1,1], [1,-1,-1], [1,-1,1], [1,1,-1], [1,1,1]])

        self.lines = [
            [0,1], [0,2], [0,4], [1,5], [1,3], [2,6],
            [2,3], [3,7], [4,5], [4,6], [5,7], [6,7]
        ]

    def _draw(self, verts):
        global GFX
        WHITE=GFX.create_pen(255, 255, 255)
        GFX.set_pen(WHITE)
        for l in self.lines:
            GFX.line(verts[l[0]][0],verts[l[0]][1], verts[l[1]][0],verts[l[1]][1])
        
