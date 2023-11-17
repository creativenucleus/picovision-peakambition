from pa_effect import paCEffect
import pa_shared_vars as shared_vars
from random import uniform
from jtruk_3d import clamp
from math import sin, cos, sqrt

class paCEffect9O(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        self.dots = []
        if iVersion == 0:
            for i in range(100):
                self.dots.append({'p': [uniform(-1, 1), uniform(-1, 1), uniform(0, 10)], 'h': uniform(0, 1), 's': 0})
        else:
            for i in range(50):
                self.dots.append({'p': [uniform(-1, 1), uniform(-1, 1), uniform(0, 10)], 'h': uniform(0, 1), 's': 0})
                self.dots.append({'p': [uniform(-1, 1), uniform(-1, 1), uniform(0, 10)], 'h': uniform(0, 1), 's': 1})

    def draw(self, gfx, display, lerpPos, tweenPos):
        portholeR = .5
        xmid, ymid = display["xmid"], display["ymid"]
        rot = sin(lerpPos * 9)*1.5 + sin(lerpPos * 5)*1.5
        sinRot, cosRot = sin(rot), cos(rot)
        for dot in self.dots:
            p = dot['p']
            p[2] -= .2
            if p[2] <= 0:
                p[2] += 10

            xd = p[0]/p[2]
            yd = p[1]/p[2]
            d = xd * xd + yd * yd
            if d > portholeR:
                continue
            x, y = int(xmid + (cosRot * xd - sinRot * yd) * xmid), int(ymid + (sinRot * xd + cosRot * yd) * ymid)

            v = 1 - clamp(p[2]/10, 0, 1)
            if dot['s'] == 1:
                v *= shared_vars.MUSIC_OUT_PULSE
            gfx.set_pen(gfx.create_pen_hsv(dot['h'], dot['s'], v))

            gfx.pixel(x, y)

    def cleanup(self):
        pass

    def legend(self):
        return "Starfield"
    
    def detail(self):
        return "A classic starfield.\nEnjoy the dots, captain.\nWarp factor something or other, I guess?!"
