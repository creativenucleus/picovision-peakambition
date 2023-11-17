from pa_effect import paCEffect
from jtruk_3d import clamp
from jtruk_3d_picovision import jtruk3DModelLetter
import pa_shared_vars as shared_vars
from math import sin, pi

class paCEffect10N(paCEffect):
    def __init__(self, iVersion):
        super().__init__()

        self.letters = []
        for i in [4,9,5,1,6,0,8,2,7,3]:
            self.letters.append(jtruk3DModelLetter(i))

    def draw(self, gfx, display, lerpPos, smoothPos):
        iDrawLetters = 10
        introTime = .25

        for i in range(0, iDrawLetters):
            tStart = (i/iDrawLetters)*introTime
            t = min((lerpPos - tStart)/introTime, 1)
            if t < 0:
                continue
            pos = self.letters[i].getFinalPos()
            dz = shared_vars.DISTANCE_START - ((1-t) * 20)
            self.letters[i].draw(gfx, display, [0,t*pi*4,t*pi*6], [pos[0], pos[1] - abs(sin(t * pi * 4))*3, pos[2] - dz], None, {
                'v': t
            })

    def legend(self):
        return ""
    
    def detail(self):
        return "That's your lot! Thanks for watching.\n\nSorry for the sound glitches! (:-o)"
