from pa_effect import paCEffect
from jtruk_3d_line import jtruk3DModelLine
from math import sin

class paCEffect1P(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
        self.iVersion = iVersion
        self.lineDefs = []
        self.farDistance = 10
        self.lineAddFreq = .05
        self.lastLineAdd = -self.lineAddFreq

    def draw(self, gfx, display, lerpPos, sweepPos):
        if self.iVersion == 0:
            camY = .7
            rotW = sin(sweepPos*20)*.1
        else:
            camY = .1 + abs(sin(sweepPos*10))*2
            rotW = sin(sweepPos*20)*.3

        camZ = sweepPos * 40
        if sweepPos - self.lastLineAdd > self.lineAddFreq:
            z = camZ + self.farDistance
            self.lineDefs.append({'line': jtruk3DModelLine(10, sweepPos, .5, z), 'z': z})
            self.lastLineAdd = sweepPos

        delLines = []
        for iLine, lineDef in enumerate(self.lineDefs):
            if lineDef['z'] >= camZ:
                lineDef['line'].draw(gfx, display, None, [0,camY,-camZ], [0,0,rotW], sweepPos)
            else:
                delLines.append(iLine)
        
        for iDelLine in delLines:
            del self.lineDefs[iDelLine]                

    def legend(self):
        return "Wave Landscape"
    
    def detail(self):
        return "This effect was sometimes driven by music, with the landscape\ndrawn from sound waves, or fractals.\nAlso used in some early games, for flying over alien planets!"


