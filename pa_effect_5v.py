from random import randint, uniform
from pa_effect import paCEffect

class paCEffect5V(paCEffect):
    def __init__(self, iVersion):
        super().__init__()

        self.dots = []
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        pen_white = gfx.create_pen(255, 255, 255)
        if randint(0,10)==0:
            self.dots.append({'x': uniform(-1, 1), 'y': -1, 'dx': uniform(-.001,.001), 'dy': 0})
        gfx.set_pen(pen_white)
        for d in self.dots:
            d['dy'] += .0002
            d['x'] += d['dx']
            d['y'] += d['dy']
            if d['y']>=1:
                del d
            else:
                x = display['xmid'] + int(d['x']*80)
                y = display['ymid'] + int(d['y']*(display['ymid']+10))
                gfx.circle(x,y,4)

    def legend(self):
        return "Bounces"
    
    def detail(self):
        return ""
