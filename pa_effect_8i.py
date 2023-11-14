from math import sin, pi
from pa_effect import paCEffect

class paCEffect8I(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        nBars = 5
        tau = pi*2
        for i in range(nBars):
            a=i*tau/(nBars)+sin(lerpPos*5)*3
            y=display['ymid'] + int(sin(a)*60)
            for ya in range(10):
                gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,ya/10))
                yline=y-ya+5
                gfx.pixel_span(0,yline, display['w'])

    def legend(self):
        return "Raster Bars"
    
    def detail(self):
        return ""
