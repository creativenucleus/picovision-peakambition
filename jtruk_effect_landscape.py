from jtruk_3d_line import jtruk3DModelLine

class jtrukEffectLandscape():
    def __init__(self, nLines):
        self.lines = []
        for iLine in range(nLines):
            self.lines.append(jtruk3DModelLine(10, iLine/nLines, iLine))

    def draw(self, gfx, display, rotL, trans, rotW, T, extra):
        for iLine, line in enumerate(self.lines):
            line.draw(gfx, display, rotL, trans, rotW, T)