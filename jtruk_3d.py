from math import floor, sin, cos, pi, sqrt

def jtruk3DSetGfx(gfx):
    global GFX
    GFX=gfx

def clamp(v,min,max):
    if v<=min:
        return min
    if v>=max:
        return max
    return v    

def makeV(x, y, z):
    return [x, y, z]

def getNormal(v1, v2, v3):
    vecA=[v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]]
    vecB=[v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2]]
    return [
        vecA[1] * vecB[2] - vecA[2] * vecB[1],
        vecA[2] * vecB[0] - vecA[0] * vecB[2],
        vecA[0] * vecB[1] - vecA[1] * vecB[0]
    ]

def getDotProduct(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

# Shorthand - add the three z points
def triZSort(tri):
    return tri['points'][0][2]+tri['points'][1][2]+tri['points'][2][2]

class jtruk3DModel:
    def __init__(self):
        self.verts = []
    
    # [[x, y, z], [x, y, z]...]
    def appendVerts(self, verts):
        self.verts.extend(verts)
    
    # display: {w}
    # trans: None or {x,y,z}
    # rot: None or {x,y,z}
    def draw(self, gfx, display, rotL, trans, rotW, T):
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
            verts.append({
                'p': [x, y, z],
                'pp': [
                    floor(display['xmid']+(x/zF)*display['scale']),
                    floor(display['ymid']+(y/zF)*display['scale']),
                    z/zF
                ]
            })

        # Draw
        self._draw(gfx, verts, T)

    def _draw(self, gfx, verts, T):
        raise Exception("There must be a _draw function for this class")


class jtruk3DModelBoxLines(jtruk3DModel):
    def __init__(self):
        super().__init__() 

        self.appendVerts([[-1,-1,-1], [-1,-1,1], [-1,1,-1], [-1,1,1], [1,-1,-1], [1,-1,1], [1,1,-1], [1,1,1]])

        self.lines = [
            [0,1], [0,2], [0,4], [1,5], [1,3], [2,6],
            [2,3], [3,7], [4,5], [4,6], [5,7], [6,7]
        ]

    def _draw(self, gfx, verts, T):
        WHITE=gfx.create_pen(255, 255, 255)
        gfx.set_pen(WHITE)
        for l in self.lines:
            gfx.line(verts[l[0]][0],verts[l[0]][1], verts[l[1]][0],verts[l[1]][1])
        

class jtruk3DModelIcosahedron(jtruk3DModel):
    def __init__(self):
        super().__init__() 

        xp=.52573
        zp=.85065
        np=0
        
        self.appendVerts([
            makeV(-xp,np,zp), makeV(xp,np,zp), makeV(-xp,np,-zp), makeV(xp,np,-zp),
            makeV(np,zp,xp), makeV(np,zp,-xp), makeV(np,-zp,xp), makeV(np,-zp,-xp),
            makeV(zp,xp,np), makeV(-zp,xp,np), makeV(zp,-xp,np), makeV(-zp,-xp,np)
        ])

        self.triangles = [
            [0,4,1], [0,9,4], [9,5,4], [4,5,8], [4,8,1],
            [8,10,1], [8,3,10], [5,3,8], [5,2,3], [2,7,3],
            [7,10,3], [7,6,10], [7,11,6], [11,0,6], [0,1,6],
            [6,1,10], [9,0,11], [9,11,2], [9,2,5], [7,2,11]
        ]
        """
        self.appendVerts([
            makeV(0,0,1),
            makeV(sqrt(8/9),0,-1/3),
            makeV(-sqrt(2/9),sqrt(2/3),-1/3),
            makeV(-sqrt(2/9),-sqrt(2/3),-1/3)
        ])
        self.triangles = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1],
            [1, 2, 3]
        ]
        """
        
    def _draw(self, gfx, verts, T):
        lightVector=[0, 0.77, -0.77]
        drawTris=[]
        totTris = len(self.triangles)
        for nTri,tri in enumerate(self.triangles):
            triV1, triV2, triV3 = verts[tri[0]], verts[tri[1]], verts[tri[2]]
            normal=getNormal(triV1['p'], triV2['p'], triV3['p'])
            
            lightStrength=clamp(getDotProduct(normal,lightVector),0,1)
            drawTris.append({
                'points': [triV1['pp'], triV2['pp'], triV3['pp']],
                'pen': gfx.create_pen_hsv(nTri/totTris, 1, clamp(lightStrength*triV1['pp'][2]/2,0.3,1)),
            })
  
        drawTris.sort(key=triZSort)
        for tri in drawTris:
            gfx.set_pen(tri['pen'])
            gfx.triangle(
                tri['points'][0][0],tri['points'][0][1],
                tri['points'][1][0],tri['points'][1][1],
                tri['points'][2][0],tri['points'][2][1],
            )
