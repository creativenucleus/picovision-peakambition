from pa_effect import paCEffect
from jtruk_3d_line import jtruk3DModelLine

class paCEffect1P(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
        nLines = 3
        self.lines = []
        for iLine in range(nLines):
            self.lines.append(jtruk3DModelLine(10, iLine/nLines, iLine))

    def draw(self, gfx, display, lerpPos, tweenPos):
        for iLine, line in enumerate(self.lines):
            line.draw(gfx, display, None, [0,0,tweenPos*5], None, tweenPos)

    def legend(self):
        return "Wave Landscape"
    
    def detail(self):
        return ""


