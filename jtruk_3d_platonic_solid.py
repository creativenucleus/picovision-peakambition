# Source from Peak Ambition (jtruk)
# License: Pirate's Honour
# You're welcome to take / copy / adapt, but please:
# 1) Drop me a little credit if you do, thanks :)
# 2) Leave this header in place, to retain the license info.
# 3) Let me know if you use / improve it!
# Full source: https://github.com/creativenucleus/picovision-peakambition/

import pa_shared_vars as shared_vars
from jtruk_3d import jtruk3DModel, makeV, getNormal, getDotProduct, triSortZ, clamp
from math import sqrt

class jtruk3DPlatonicSolid(jtruk3DModel):
    def __init__(self, iModel):
        super().__init__() 

        xp=.52573
        zp=.85065
        np=0
        
        if iModel == 0:
            # Tetrahedron
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
        else:
            # Icosahedron
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

    def _draw(self, gfx, verts, extra):
        pulseMult = .3 + .7*shared_vars.MUSIC_OUT_PULSE
        lightVector=[0, 0.77, -0.77]
        drawTris=[]
        totTris = len(self.triangles)
        for nTri,tri in enumerate(self.triangles):
            triV1, triV2, triV3 = verts[tri[0]], verts[tri[1]], verts[tri[2]]
            normal=getNormal(triV1['p'], triV2['p'], triV3['p'])
            
            lightStrength=clamp(getDotProduct(normal,lightVector),0,1)
            if extra['pulse']:
                triType = nTri % 3
                if triType == 0:
                    pen = gfx.create_pen_hsv(nTri/totTris, 0.5, clamp(lightStrength*triV1['pp'][2]/2,0.1,1)*pulseMult)
                elif triType == 1:
                    continue    # skip this face
                else:
                    pen = gfx.create_pen_hsv(nTri/totTris, 1, clamp(lightStrength*triV1['pp'][2]/2,0.1,1)*pulseMult)
            else:
                pen = gfx.create_pen_hsv(nTri/totTris, 1, clamp(lightStrength*triV1['pp'][2]/2,0.1,1))

            drawTris.append({
                'points': [triV1['pp'], triV2['pp'], triV3['pp']],
                'z': triV1['p'][2] + triV2['p'][2] + triV3['p'][2],
                'pen': pen,
            })
  
        drawTris.sort(key=triSortZ)
        for tri in drawTris:
            gfx.set_pen(tri['pen'])
            gfx.triangle(
                tri['points'][0][0],tri['points'][0][1],
                tri['points'][1][0],tri['points'][1][1],
                tri['points'][2][0],tri['points'][2][1],
            )
