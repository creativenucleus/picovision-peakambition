# Source from Peak Ambition (jtruk)
# License: Pirate's Honour
# You're welcome to take / copy / adapt, but please:
# 1) Drop me a little credit if you do, thanks :)
# 2) Leave this header in place, to retain the license info.
# 3) Let me know if you use / improve it!
# Full source: https://github.com/creativenucleus/picovision-peakambition/

from math import sin
from pa_effect import paCEffect
import pa_shared_vars as shared_vars

class paCEffect7S(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        self.iVersion = iVersion
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        nBobs=20
        for i in range(nBobs):
            x=display['xmid'] + int(sin(i*.35+lerpPos*25)*120*lerpPos)
            y=display['ymid'] + +int(sin(i*.2+lerpPos*40)*80*lerpPos)
            s = 8
            ofs = 4
            if self.iVersion == 1 and i % 2 == 0:
                s = 3 + shared_vars.MUSIC_OUT_PULSE * 5
                ofs = int(4 * s/8)

            h = i/nBobs + s*.1
            gfx.set_pen(gfx.create_pen_hsv(h,1,.6))
            gfx.circle(x-1,y-1,int(s))
            gfx.set_pen(gfx.create_pen_hsv(h,.8,1))
            gfx.circle(x-ofs,y-ofs,int(s * 3/8))

    def legend(self):
        return "Bobs"
    
    def detail(self):
        return "Some 80s/90s machines had hardware sprites\nFolks competed to show the most simultaneously with hacks\nOften the bobbed around\n...But the name comes from 'Blitter Object'"
