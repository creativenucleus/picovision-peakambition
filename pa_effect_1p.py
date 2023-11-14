from pa_effect import paCEffect
from jtruk_3d_line import jtruk3DModelLine
from math import sin

class paCEffect1P(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
        self.lineDefs = []
        self.farDistance = 10
        self.lineAddFreq = .05
        self.lastLineAdd = -self.lineAddFreq

    def draw(self, gfx, display, lerpPos, tweenPos):
        camZ = tweenPos * 40
        if tweenPos - self.lastLineAdd > self.lineAddFreq:
            z = camZ + self.farDistance
            self.lineDefs.append({'line': jtruk3DModelLine(10, tweenPos, .5, z), 'z': z})
            self.lastLineAdd = tweenPos

        delLines = []
        rotW = sin(tweenPos*40)*.3
        for iLine, lineDef in enumerate(self.lineDefs):
            if lineDef['z'] >= camZ:
                lineDef['line'].draw(gfx, display, None, [0,.7,-camZ], [0,0,rotW], tweenPos)
            else:
                delLines.append(iLine)
        
        for iDelLine in delLines:
            del self.lineDefs[iDelLine]                

    def legend(self):
        return "Wave Landscape"
    
    def detail(self):
        return ""


