from jtruk_3d import jtruk3DModel, makeV, clamp
from math import sin, cos, pi, sqrt

class jtruk3DModelPicovision(jtruk3DModel):
    def __init__(self):
        super().__init__()
        
        self.letters=[
            {'vs': transVs(makeLetter('P'), 0, 0, 0), 'o': makeV(0,-.5,0)},
            {'vs': transVs(makeLetter('I'), 1.5, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('C'), 3, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('O'), 5, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('V'), 7, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('I'), 8.5, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('S'), 10, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('I'), 11.5, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('O'), 13, 0, 0), 'o': makeV(0,0,0)},
            {'vs': transVs(makeLetter('N'), 15.5, 0, 0), 'o': makeV(.5,-.5,0)}
        ]

        self.iLetterDef=[]
        for l in self.letters:
            startVert=len(self.verts)
            transL=transVs(l['vs'], -7.78, 0, 0)
            self.appendVerts(transL)
            endVert=len(self.verts)
            self.iLetterDef.append({'vs': [startVert, endVert], 'mid': addV3(getMidV(transL), l['o'])})

    def getLetterPos(self, i):
        return self.iLetterDef[i]['mid']
        
    def getLetterVertexSpan(self, i):
        return self.iLetterDef[i]['vs']

    def _draw(self, gfx, verts, extra):
        # Global line thickness (as approximation)
        v = verts[self.iLetterDef[0]['vs'][0]]
        thickness = int(sqrt(clamp(v['pp'][2]*4,4,16)))

        allLines=[]
        for iLetter, vertDef in enumerate(self.iLetterDef):

            # Collect the lines for one letter
            letterLines=[]
            vLast = None
            for iV in range(vertDef['vs'][0],vertDef['vs'][1]):
                v = verts[iV]
                if vLast != None:
                    hue=iV*0.002+extra['t']*0.015
                    line={
                        'h': hue,
                        'i': 1 if (extra['focusLetter']==iLetter) else extra['otherIntensity'],
                        'x0': v['pp'][0], 'y0': v['pp'][1],
                        'x1': vLast['pp'][0], 'y1': vLast['pp'][1],
                        't': thickness
                    }
                    letterLines.append(line)
                vLast=v
            allLines.append(letterLines)

        self.drawLines(allLines, gfx, 0, len(self.iLetterDef))
        return allLines
    
    def drawLines(self, allLines, gfx, lStart, lEnd):
        for iLetter in range(lStart, lEnd):
            for l in allLines[iLetter]:
                gfx.set_pen(gfx.create_pen_hsv(l['h'],1,l['i']))
                gfx.line(l['x0'],l['y0'],l['x1'],l['y1'],l['t'])
        

def makeLetter(letter):
    if letter=='P':
        return (
            [makeV(-1,1,0), makeV(-1,-1,0), makeV(0,-1,0)] +
            transVs(scaleV(getPointsArc(8,pi*2.5,pi*1.5),1,.5,1),0,-.5,0) +
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
            transVs(scaleV(getPointsArc(8,0,pi*1.5),1,.5,1),0,-.5,0) +
            transVs(scaleV(getPointsArc(8,pi*.5,-pi*1),1,.5,1),0,.5,0)
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

# Add two vectors
def addV3(v0, v1):
    return [v0[0] + v1[0], v0[1] + v1[1], v0[2] + v1[2]]

# Translate a bunch of verts
def transVs(vs, x,y,z):
    for v in vs:
        v[0] += x
        v[1] += y
        v[2] += z
    return vs

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