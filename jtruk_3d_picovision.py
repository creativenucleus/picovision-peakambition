from jtruk_3d import jtruk3DModel, makeV, clamp
from math import sin, cos, pi, sqrt

class jtruk3DModelPicovision(jtruk3DModel):
    def __init__(self):
        super().__init__()
        
        self.letters=[
            transV(makeLetter('P'), 0, 0, 0),
            transV(makeLetter('I'), 1.5, 0, 0),
            transV(makeLetter('C'), 3, 0, 0),
            transV(makeLetter('O'), 5, 0, 0),
            transV(makeLetter('V'), 7, 0, 0),
            transV(makeLetter('I'), 8.5, 0, 0),
            transV(makeLetter('S'), 10, 0, 0),
            transV(makeLetter('I'), 11.5, 0, 0),
            transV(makeLetter('O'), 13, 0, 0),
            transV(makeLetter('N'), 15.5, 0, 0),
        ]

        self.iLetterDef=[]
        for l in self.letters:
            startVert=len(self.verts)
            transL=transV(l, -7.78, 0, 0)
            self.appendVerts(transL)
            endVert=len(self.verts)
            self.iLetterDef.append({'vs': [startVert, endVert], 'mid': getMidV(transL)})
            
    def getLetterPos(self, i):
        return self.iLetterDef[i]['mid']
        
    def _draw(self, gfx, verts, T):
        gfx.set_pen(gfx.create_pen_hsv(1, 1, 1))
        for vertDef in self.iLetterDef:
            vLast = None
            for iV in range(vertDef['vs'][0],vertDef['vs'][1]):
                v = verts[iV]
                if vLast != None:
                    gfx.set_pen(gfx.create_pen_hsv(iV*0.002+T*0.015,1,1))
                    gfx.line(
                        v['pp'][0],
                        v['pp'][1],
                        vLast['pp'][0],
                        vLast['pp'][1],int(sqrt(clamp(v['pp'][2]*4,4,16)))
                    )
                vLast=v

def makeLetter(letter):
    if letter=='P':
        return (
            [makeV(-1,1,0), makeV(-1,-1,0), makeV(0,-1,0)] +
            transV(scaleV(getPointsArc(8,pi*2.5,pi*1.5),1,.5,1),0,-.5,0) +
            [makeV(-1,0,0)]
        )
    elif letter=='I':
        return [makeV(0,-1,0),makeV(0,1,0)]
    elif letter=='C':
        return getPointsArc(12,pi*.25,pi*2-pi*.25)
    elif letter=='O':
        return getPointsArc(16,0,pi*2)
    elif letter=='V':
        return [makeV(-1,-1,0),makeV(0,1,0),makeV(1,-1,0)]
    if letter=='S':
        return (
            transV(scaleV(getPointsArc(8,0,pi*1.5),1,.5,1),0,-.5,0) +
            transV(scaleV(getPointsArc(8,pi*.5,-pi*1),1,.5,1),0,.5,0)
        )
    elif letter=='N':
        return [makeV(-1,1,0),makeV(-1,-1,0),makeV(1,1,0),makeV(1,-1,0)]

def getPointsArc(nPoints,a0,a1):
    points=[]
    for a in range(nPoints+1):
        a=a0+(a/(nPoints))*(a1-a0)
        x=cos(a)
        y=-sin(a)
        points.append(makeV(x,y,0))
    return points

# Translate a bunch of verts
def transV(verts, x,y,z):
    for v in verts:
        v[0] += x
        v[1] += y
        v[2] += z
    return verts

# Scale a bunch of verts
def scaleV(verts, sX,sY,sZ):
    for v in verts:
        v[0] *= sX
        v[1] *= sY
        v[2] *= sZ
    return verts

# Returns the mid point x,y,z
def getMidV(verts):
    vMin, vMax = None, None

    for v in verts:
        if vMin == None:
            vMin, vMax = v, v
        else:
            vMin=makeV(min(vMin[0],v[0]), min(vMin[1],v[1]), min(vMin[2],v[2]))
            vMax=makeV(max(vMax[0],v[0]), max(vMax[1],v[1]), max(vMax[2],v[2]))
    return makeV((vMin[0]+vMax[0])/2, (vMin[1]+vMax[1])/2, (vMin[2]+vMax[2])/2)