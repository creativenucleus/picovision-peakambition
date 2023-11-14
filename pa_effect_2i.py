from math import sin, cos
from pa_effect import paCEffect

class paCEffect2I(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        baseA=sin(lerpPos*10)*2
        for y in range(display['h']/3):
            yline=y*3
            a=baseA+y*0.01+sin(yline*.01+lerpPos*14)*2
            w=80*tweenPos
            xc=display['xmid']+sin(yline*.015+lerpPos*20)*40*lerpPos
            sina=sin(a)
            cosa=cos(a)
            x0=int(xc+sina*w)
            x1=int(xc+cosa*w)
            x2=int(xc-sina*w)
            x3=int(xc-cosa*w)
            cshift=lerpPos+y*.005

            if x1>x0:
                gfx.set_pen(gfx.create_pen_hsv(0+cshift,1,-sina*.5+.5))
                gfx.pixel_span(x0,yline,x1-x0)
            if x2>x1:
                gfx.set_pen(gfx.create_pen_hsv(0.25+cshift,1,-cosa*.5+.5))
                gfx.pixel_span(x1,yline,x2-x1)
            if x3>x2:
                gfx.set_pen(gfx.create_pen_hsv(0.5+cshift,1,sina*.5+.5))
                gfx.pixel_span(x2,yline,x3-x2)
            if x0>x3:
                gfx.set_pen(gfx.create_pen_hsv(0.75+cshift,1,cosa*.5+.5))
                gfx.pixel_span(x3,yline,x0-x3)

    def legend(self):
        return "Twister"
    
    def detail(self):
        return "What an amazing effect\nDoes this spread over two lines?"