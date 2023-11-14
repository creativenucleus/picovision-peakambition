from math import sin
from pa_effect import paCEffect
import pa_shared_vars as shared_vars

class paCEffect9O(paCEffect):
    def __init__(self, iVersion):
        super().__init__()
        _ = shared_vars.SPRITES.add(shared_vars.GFX, shared_vars.SPR_PIRATE, 32, 32)
        
    def draw(self, gfx, display, lerpPos, tweenPos):
        for i in range(0,19):
            shared_vars.SPRITES.set(gfx, i, shared_vars.SPR_PIRATE, int(32+sin(tweenPos*20 + i*.2)*40+100), int(32+sin(tweenPos*15 + i*.22)*40+100), blend=1)

    def cleanup(self):
        shared_vars.SPRITES.removeAll(shared_vars.GFX)

    def legend(self):
        return ""
    
    def detail(self):
        return ""
