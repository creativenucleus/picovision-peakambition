from jtruk_3d import jtruk3DModel, makeV, clamp
from math import sin, cos, pi, sqrt

LETTERS = [
    {'l': 'P', 't': [0,0,0], 'o': [0,-.5,0]},
    {'l': 'I', 't': [1.5,0,0], 'o': [0,0,0.02]},
    {'l': 'C', 't': [3,0,0], 'o': [0,0,0]},
    {'l': 'O', 't': [5,0,0], 'o': [0,0,0]},
    {'l': 'V', 't': [7,0,0], 'o': [0,0,-.5]},
    {'l': 'I', 't': [8.5,0,0], 'o': [0,0,0.02]},
    {'l': 'S', 't': [10,0,0], 'o': [0,0,0]},
    {'l': 'I', 't': [11.5,0,0], 'o': [0,0,0.35]},
    {'l': 'O', 't': [13,0,0], 'o': [0,0,0]},
    {'l': 'N', 't': [15.5,0,0], 'o': [.5,-.5,0]},
]

for letter in LETTERS:
    letter['t'] = [letter['t'][0] - 7.78, letter['t'][1], letter['t'][2]]

class jtruk3DModelPicovision(jtruk3DModel):
    def __init__(self):
        super().__init__()

        self.iLetterDef=[]
        for _, l in enumerate(LETTERS):
            startVert=len(self.verts)
            vs = transVs(makeLetter(l['l']), l['t'][0], l['t'][1], l['t'][2])
            self.appendVerts(vs)
            endVert=len(self.verts)
            self.iLetterDef.append({'vs': [startVert, endVert], 'mid': addV3(getMidV(vs), l['o'])})

    def getLetterPos(self, i):
        return self.iLetterDef[i]['mid']
        
    def getLetterVertexSpan(self, i):
        return self.iLetterDef[i]['vs']

    def _draw(self, gfx, verts, extra):
        allLines=[]
        thickness = None
        for iLetter, vertDef in enumerate(self.iLetterDef):
            # Collect the lines for one letter
            letterLines=[]
            vLast = None
            for iV in range(vertDef['vs'][0], vertDef['vs'][1]):
                v = verts[iV]
                if thickness == None:
                    thickness = clamp(int(sqrt(25/(v['p'][2]))), 2, 5)

                if vLast != None:
                    if iLetter == extra['focusLetter']:
                        if iLetter == 9 and iV == 70 or iV == 72:
                            intensity = .2
                        intensity = 1
                    else:
                        intensity = extra['otherIntensity']

                    hue=iV*0.002+extra['t']*0.015
                    line={
                        'h': hue,
                        'i': intensity,
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

class jtruk3DModelLetter(jtruk3DModel):
    def __init__(self, iLetter):
        super().__init__()
        self.iLetter = iLetter
        letter = LETTERS[iLetter]
        vs = makeLetter(letter['l'])
        self.appendVerts(vs)

    def getFinalPos(self):
        return LETTERS[self.iLetter]['t']

    def _draw(self, gfx, verts, extra):
        gfx.set_pen(gfx.create_pen_hsv(0,1,extra['v']))
        vLast = None
        for v in verts:
            if vLast != None:
                gfx.line(v['pp'][0],v['pp'][1], vLast['pp'][0],vLast['pp'][1], 2)
            vLast = v

def makeLetter(letter):
    if letter=='P':
        return (
            [makeV(-1,1,0), makeV(-1,-1,0), makeV(0,-1,0)] +
            transVs(scaleV(getPointsArc(6,pi*2.5,pi*1.5),1,.5,1),0,-.5,0) +
            [makeV(-1,0,0)]
        )
    elif letter=='I':
        return [makeV(0,-1,0),makeV(0,1,0)]
    elif letter=='C':
        return getPointsArc(12,pi*.25,pi*2-pi*.25)
    elif letter=='O':
        return getPointsArc(10,0,pi*2)
    elif letter=='V':
        return [makeV(-1,-1,0),makeV(0,1,0),makeV(1,-1,0)]
    if letter=='S':
        return (
            transVs(scaleV(getPointsArc(6,0,pi*1.5),1,.5,1),0,-.5,0) +
            transVs(scaleV(getPointsArc(6,pi*.5,-pi*1),1,.5,1),0,.5,0)
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