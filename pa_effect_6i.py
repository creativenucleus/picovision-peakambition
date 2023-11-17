from math import sin, cos
from pa_effect import paCEffect
import pa_shared_vars as shared_vars

class paCEffect6I(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        self.iVersion = iVersion
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        nBars=20
        xmid = display["xmid"]
        for i in range(nBars):
            x=xmid+int(sin(i*.07+lerpPos*36)*60+cos(i*.15+lerpPos*25)*20)
            y=70+i*4
            if self.iVersion == 0:
                gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,i/nBars))
            else:
                if i % 2 == 0:
                    gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,(i/nBars) * .3))
                else:
                    gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,(i/nBars) * shared_vars.MUSIC_OUT_PULSE))
            gfx.rectangle(x-4,y,8, display['h']-y)

    def legend(self):
        return "Alcatraz Bars"
    
    def detail(self):
        return "Also known by some as Kefrens Bars or Raster Bars.\nThis effect benefitted from the vertical draw of the screen\nbuilding up each time\n...but I'm cheating and using rectangles! :)"
