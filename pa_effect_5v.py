from random import uniform
from pa_effect import paCEffect
from jtruk_3d import lineIntersect
import pa_shared_vars as shared_vars

class paCEffect5V(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        self.dotStartDx = [-.019, .017, -.007]
        self.dotAddInterval = 0.15
        self.dotAddLast = -self.dotAddInterval

        self.dots = []
        
    def draw(self, gfx, display, lerpPos, sweepPos):
        if lerpPos >= self.dotAddLast + self.dotAddInterval and len(self.dots) < len(self.dotStartDx):
            self.dots.append({'x': 0, 'y': -.6, 'dx': self.dotStartDx[len(self.dots)], 'dy': .02})
            self.dotAddLast = self.dotAddLast + self.dotAddInterval

        gfx.set_pen(gfx.create_pen(255, 255, 255))
        buffer = .09 # cater for circle radius
        tx0,ty0, tx1,ty1, tx2, ty2= -1, -.7 - buffer, 0, .7 - buffer, 1, -.7 - buffer
        """
        # DEBUG LINES
        gfx.line(
            display['xmid'] + int(tx0 *80),
            display['ymid'] + int(ty0 *(display['ymid'])),
            display['xmid'] + int(tx1 *80),
            display['ymid'] + int(ty1 *(display['ymid']))
        )

        gfx.line(
            display['xmid'] + int(tx1 *80),
            display['ymid'] + int(ty1 *(display['ymid'])),
            display['xmid'] + int(tx2 *80),
            display['ymid'] + int(ty2 *(display['ymid']))
        )
        """
        
        for i, d in enumerate(self.dots):
            gfx.set_pen(gfx.create_pen_hsv(i/3, 1, .2 + shared_vars.MUSIC_OUT_PULSE*.8))
            newX, newY = d['x']+d['dx'], d['y']+d['dy']
            if d['x'] <= 0:
                isI = lineIntersect(d['x'],d['y'], newX,newY, tx0,ty0, tx1,ty1)
                if isI and d['dx'] < 0:
                    d['dx'] = -d['dx']
            else:
                isI = lineIntersect(d['x'],d['y'], newX,newY, tx1,ty1, tx2,ty2)
                if isI and d['dx'] > 0:
                    d['dx'] = -d['dx']

            if isI:
                # absorb some energy
                d['dy'] = -d['dy']*.6
            else:
                d['dy'] += .0002

            d['x'] += d['dx']
            d['y'] += d['dy']
            if d['y']>=1:
                del d
            else:
                x = display['xmid'] + int(d['x']*80)
                y = display['ymid'] + int(d['y']*(display['ymid']))
                gfx.circle(x,y,6)

    def legend(self):
        return "Bounces"
    
    def detail(self):
        return ""
