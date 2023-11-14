from math import sin, cos, pi, fmod
from pa_effect import paCEffect

class paCEffect4O(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        t=tweenPos * 50
        for iD in range(10):
            d=pow(fmod(iD/10 + t*.03, 1),2)
            for iA in range(10):
                a=iA/10*pi*2+iD*.2+t*.02
                gfx.set_pen(gfx.create_pen_hsv(iA*.1+iD*.2,1,d))
                x=int((sin(1/(iD+1)*t*.01)*d*50)+(sin(a)*d*180))
                y=int(cos(a)*d*140)
                gfx.circle(display['xmid'] + x, display['ymid'] + y, int(4*d))
                #gfx.pixel(WHALF+x,HHALF+y)

    def legend(self):
        return "Dot Tunnel"
    
    def detail(self):
        return ""

