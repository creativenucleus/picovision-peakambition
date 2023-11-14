from pa_effect import paCEffect
from jtruk_3d_picovision import jtruk3DModelLetter
import pa_shared_vars as shared_vars

class paCEffect10N(paCEffect):
    def __init__(self, iVersion):
        super().__init__()

        self.letters = []
        for i in range(0,10):
            self.letters.append(jtruk3DModelLetter(i))
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        iDrawLetters = 10
        if lerpPos < .5:
            iDrawLetters = int(lerpPos/.5*iDrawLetters)

        dz = shared_vars.DISTANCE_START
        for i in range(0, iDrawLetters):
            pos = self.letters[i].getFinalPos()
            self.letters[i].draw(gfx, display, None, [pos[0], pos[1], pos[2] - dz], None)

    def legend(self):
        return ""
    
    def detail(self):
        return ""
