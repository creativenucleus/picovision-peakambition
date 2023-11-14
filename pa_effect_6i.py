from math import sin
from pa_effect import paCEffect

class paCEffect6I(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        nBars=20
        for i in range(nBars):
            x=120+int(sin(i*.07+lerpPos*16)*40+sin(i*.12+lerpPos*25)*40)
            y=70+i*4
            gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,i/nBars))
            gfx.rectangle(x-4,y,8, display['h']-y)

    def legend(self):
        return "Alcatraz Bars"
    
    def detail(self):
        return ""
