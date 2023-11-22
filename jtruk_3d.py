# Source from Peak Ambition (jtruk)
# License: Pirate's Honour
# You're welcome to take / copy / adapt, but please:
# 1) Drop me a little credit if you do, thanks :)
# 2) Leave this header in place, to retain the license info.
# 3) Let me know if you use / improve it!
# Full source: https://github.com/creativenucleus/picovision-peakambition/

from math import floor, sin, cos

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
def triSortZ(tri):
    return tri['z']

def det(a, b, c, d):
    return a * d - b * c

# https://jvm-gaming.org/t/fastest-linesintersect-method/35387
def lineIntersect(x1, y1, x2, y2, x3, y3, x4, y4):
    if (x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4):
        return False
    
    # Fastest method, based on Franklin Antonio's "Faster Line Segment Intersection" topic "in Graphics Gems III" book (http://www.graphicsgems.org/)
    ax = x2-x1
    ay = y2-y1
    bx = x3-x4
    by = y3-y4
    cx = x1-x3
    cy = y1-y3

    alphaNumerator = by*cx - bx*cy
    commonDenominator = ay*bx - ax*by
    if commonDenominator > 0:
        if alphaNumerator < 0 or alphaNumerator > commonDenominator:
            return False
    elif commonDenominator < 0:
        if alphaNumerator > 0 or alphaNumerator < commonDenominator:
            return False
    betaNumerator = ax*cy - ay*cx
    if commonDenominator > 0:
        if betaNumerator < 0 or betaNumerator > commonDenominator:
            return False
    elif commonDenominator < 0:
        if betaNumerator > 0 or betaNumerator < commonDenominator:
            return False
    if commonDenominator == 0:
        # This code wasn't in Franklin Antonio's method. It was added by Keith Woodward.
        # The lines are parallel.
        # Check if they're collinear.
        y3LessY1 = y3-y1
        collinearityTestForP3 = x1*(y2-y3) + x2*(y3LessY1) + x3*(y1-y2)	# see http://mathworld.wolfram.com/Collinear.html
        # If p3 is collinear with p1 and p2 then p4 will also be collinear, since p1-p2 is parallel with p3-p4
        if collinearityTestForP3 == 0:
            # The lines are collinear. Now check if they overlap.
            if (x1 >= x3 and x1 <= x4 or x1 <= x3 and x1 >= x4 or
              x2 >= x3 and x2 <= x4 or x2 <= x3 and x2 >= x4 or
              x3 >= x1 and x3 <= x2 or x3 <= x1 and x3 >= x2
            ):
                if (y1 >= y3 and y1 <= y4 or y1 <= y3 and y1 >= y4 or
                    y2 >= y3 and y2 <= y4 or y2 <= y3 and y2 >= y4 or
                    y3 >= y1 and y3 <= y2 or y3 <= y1 and y3 >= y2
                ):
                    return True
        return False
    return True


# https://jvm-gaming.org/t/fastest-linesintersect-method/35387
def lineIntersectPoint(x1, y1, x2, y2, x3, y3, x4, y4):
    det1And2 = det(x1, y1, x2, y2)
    det3And4 = det(x3, y3, x4, y4)
    x1LessX2 = x1 - x2
    y1LessY2 = y1 - y2
    x3LessX4 = x3 - x4
    y3LessY4 = y3 - y4
    det1Less2And3Less4 = det(x1LessX2, y1LessY2, x3LessX4, y3LessY4)
    if (det1Less2And3Less4 == 0):
        # the denominator is zero so the lines are parallel and there's either no solution (or multiple solutions if the lines overlap) so return null.
        return False, 0, 0
    x = (det(det1And2, x1LessX2, det3And4, x3LessX4) / det1Less2And3Less4)
    y = (det(det1And2, y1LessY2, det3And4, y3LessY4) / det1Less2And3Less4)
    return True, x, y

class jtruk3DModel:
    def __init__(self):
        self.verts = []
    
    # [[x, y, z], [x, y, z]...]
    def appendVerts(self, verts):
        self.verts.extend(verts)
    
    # display: {w}
    # rotL: None or [x,y,z]
    # trans: None or [x,y,z]
    # rotW: None or [x,y,z]
    # We can return stuff from the _draw function if we need transitions
    def draw(self, gfx, display, rotL, trans, rotW, extra=None):
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
                                
            zF=(.001 if z==0 else z)/1.5
            verts.append({
                'p': [x, y, z],
                'pp': [
                    floor(display['xmid']+(x/zF)*display['scale']),
                    floor(display['ymid']+(y/zF)*display['scale']),
                    z/zF
                ]
            })

        return self._draw(gfx, verts, extra)

    def _draw(self, gfx, verts, extra):
        raise Exception("There must be a _draw function for this class")


class jtruk3DModelBoxLines(jtruk3DModel):
    def __init__(self):
        super().__init__() 

        self.appendVerts([[-1,-1,-1], [-1,-1,1], [-1,1,-1], [-1,1,1], [1,-1,-1], [1,-1,1], [1,1,-1], [1,1,1]])

        self.lines = [
            [0,1], [0,2], [0,4], [1,5], [1,3], [2,6],
            [2,3], [3,7], [4,5], [4,6], [5,7], [6,7]
        ]

    def _draw(self, gfx, verts, extra):
        WHITE=gfx.create_pen(255, 255, 255)
        gfx.set_pen(WHITE)
        for l in self.lines:
            gfx.line(verts[l[0]][0],verts[l[0]][1], verts[l[1]][0],verts[l[1]][1])
