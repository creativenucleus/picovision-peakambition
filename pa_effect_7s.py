from math import sin
from pa_effect import paCEffect

class paCEffect7S(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        nBobs=20
        for i in range(nBobs):
            x=display['xmid'] + int(sin(i*.35+lerpPos*25)*120*lerpPos)
            y=display['ymid'] + +int(sin(i*.2+lerpPos*40)*80*lerpPos)
            gfx.set_pen(gfx.create_pen_hsv(i/nBobs,1,.6))
            gfx.circle(x-1,y-1,8)
            gfx.set_pen(gfx.create_pen_hsv(i/nBobs,.8,1))
            gfx.circle(x-4,y-4,3)

    def legend(self):
        return "Bobs"
    
    def detail(self):
        return ""
