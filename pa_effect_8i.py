# Source from Peak Ambition (jtruk)
# License: Pirate's Honour
# You're welcome to take / copy / adapt, but please:
# 1) Drop me a little credit if you do, thanks :)
# 2) Leave this header in place, to retain the license info.
# 3) Let me know if you use / improve it!
# Full source: https://github.com/creativenucleus/picovision-peakambition/

from math import sin, pi
from pa_effect import paCEffect
import pa_shared_vars as shared_vars

class paCEffect8I(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        self.iVersion = iVersion

    def draw(self, gfx, display, lerpPos, sweepPos):
        nBars = 5
        tau = pi*2

        cshift = 0
        if self.iVersion == 1:
            cshift = shared_vars.MUSIC_OUT_PULSE

        for i in range(nBars):
            a=i*tau/(nBars)+sin(lerpPos*5)*3
            y=display['ymid'] + int(sin(a)*(40*sweepPos + 20))
            for ya in range(10):
                gfx.set_pen(gfx.create_pen_hsv(i/nBars,1 - cshift,ya/10))
                yline=y-ya+5
                gfx.pixel_span(0,yline, display['w'])

    def legend(self):
        return "Raster Bars"
    
    def detail(self):
        return "The vertical redraw timing of the screen on 16bit computers\ngave demo coders a little extra window of time to play\nThe Amiga was expecially known for these techniques"
