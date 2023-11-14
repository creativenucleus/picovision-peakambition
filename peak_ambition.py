from picographics import PicoGraphics, PEN_RGB555
from math import sin, pi
from time import ticks_cpu
import _thread
from jtruk_sprite import jtrukSpriteModel, jtrukSprites
from jtruk_music_player import MusicPlayer
from jtruk_3d_picovision import jtruk3DModelPicovision
from jtruk_tune_main import tune as main_tune
import pa_shared_vars as shared_vars
from pa_effect_1p import paCEffect1P
from pa_effect_2i import paCEffect2I
from pa_effect_3c import paCEffect3C
from pa_effect_4o import paCEffect4O
from pa_effect_5v import paCEffect5V
from pa_effect_6i import paCEffect6I
from pa_effect_7s import paCEffect7S
from pa_effect_8i import paCEffect8I
from pa_effect_9o import paCEffect9O
from pa_effect_10n import paCEffect10N
from jtruk_3d import makeV

gfx=PicoGraphics(pen_type=PEN_RGB555, width=320, height=240)

shared_vars.GFX = gfx

#gfx=PicoGraphics(pen_type=PEN_RGB555, width=640, height=480)
WIDTH,HEIGHT=gfx.get_bounds()
DISPLAY={'w': WIDTH, 'h': HEIGHT, 'xmid': int(WIDTH/2), 'ymid': int(HEIGHT/2), 'scale': 100}
tau=pi*2
WHALF=int(WIDTH/2)
HHALF=int(HEIGHT/2)
BLACK=gfx.create_pen(0, 0, 0)
WHITE=gfx.create_pen(255, 255, 255)
RED=gfx.create_pen(255, 0, 0)
T=0

SPRITES = jtrukSprites(20)
shared_vars.SPRITES = SPRITES

SPR_PIRATE_MODEL_ID = 0

SCRIPT=[
    {'action':"move", 'letter':0, 'rz': -pi*.5},
    {'action':"effect", 'ceffect':paCEffect1P, 'duration': 300},
    {'action':"move", 'letter':1, 'rz': pi},
    {'action':"effect", 'ceffect':paCEffect2I, 'duration': 100},
    {'action':"move", 'letter':2, 'rz': -pi*.5},
    {'action':"effect", 'ceffect':paCEffect3C, 'duration': 100},
    {'action':"move", 'letter':3, 'rz': -pi*1.25},
    {'action':"effect", 'ceffect':paCEffect4O, 'duration': 100},
    {'action':"move", 'letter':4, 'rz': 0},
    {'action':"effect", 'ceffect':paCEffect5V, 'duration': 100},
    {'action':"move", 'letter':5, 'rz': pi},
    {'action':"effect", 'ceffect':paCEffect6I, 'duration': 100},
    {'action':"move", 'letter':6, 'rz': -pi*.5},
    {'action':"effect", 'ceffect':paCEffect7S, 'duration': 100},
    {'action':"move", 'letter':7, 'rz': -pi*1.5},
    {'action':"effect", 'ceffect':paCEffect8I, 'duration': 100},
    {'action':"move", 'letter':8, 'rz': -pi*1.75},
    {'action':"effect", 'ceffect':paCEffect9O, 'duration': 100},
    {'action':"move", 'letter':9, 'rz': -pi*.25},
    {'action':"effect", 'ceffect':paCEffect10N, 'duration': 100},
]

SCRIPT_POS=-1
SCRIPT_ACTION_CAP=10
SCRIPT_ACTION_T=SCRIPT_ACTION_CAP
SCRIPT_ITEM=None
CAM={'p': makeV(0,0,0), 'rz': 0}
CAM_TWEEN0={'p': makeV(0,0,0), 'rz': 0}
CAM_TWEEN1={'p': makeV(0,0,0), 'rz': 0}
EFFECT=None
ILOOP=0
PICOVISION=jtruk3DModelPicovision()


def doScript(lerpPos, tweenPos):
    global SCRIPT_ITEM, SCRIPT_ACTION_T
    global CAM, CAM_TWEEN0, CAM_TWEEN1
    global EFFECT
    if SCRIPT_ITEM['action'] == "move":
        if SCRIPT_ACTION_T==0:
            CAM_TWEEN0=CAM
            letter=PICOVISION.getLetterPos(SCRIPT_ITEM['letter'])
            CAM_TWEEN1={'p': makeV(letter[0], letter[1], -9.25), 'rz': SCRIPT_ITEM['rz']}
        CAM={
            'p': makeV(
                lerp(tweenPos, CAM_TWEEN0['p'][0], CAM_TWEEN1['p'][0]),
                lerp(tweenPos, CAM_TWEEN0['p'][1], CAM_TWEEN1['p'][1]),
                lerp(tweenPos, CAM_TWEEN0['p'][2], CAM_TWEEN1['p'][2]) + sin(tweenPos*pi)*10
            ),
            'rz': lerp(tweenPos, CAM_TWEEN0['rz'], CAM_TWEEN1['rz'])
        }
    elif SCRIPT_ITEM['action'] == "effect":
        if SCRIPT_ACTION_T == 0:
            EFFECT=SCRIPT_ITEM['ceffect'](ILOOP)

        EFFECT.draw(gfx, DISPLAY, lerpPos, tweenPos)
        legend = EFFECT.legend()
        detail = EFFECT.detail()
        x,y=WHALF-len(legend)*7,10
        xl,yl=20,HEIGHT-20
        gfx.set_pen(RED)
        gfx.text(legend, x+1,y+1)
        gfx.set_pen(BLACK)
        gfx.text(detail, xl+1,yl+1, scale=1)
        gfx.set_pen(WHITE)
        gfx.text(legend, x,y)
        gfx.text(detail, xl,yl, scale=1)
    return lerpPos, tweenPos

def debugPrintScript():
    global SCRIPT_POS, SCRIPT_ACTION_T
    gfx.text("POS {} T {}".format(SCRIPT_POS, SCRIPT_ACTION_T), 0,10, fixed_width=1,scale=1)
    
def lerp(t,v1,v2):
    return (1-t)*v1+t*v2

def smoothStep(t):
    return t * t * (3.0 - 2.0 * t)

def rampUpThenDown(t):
    if t<.2:
        return t/.2
    elif t>.8:
        return (1-t)/.2
    else:
        return 1

def preflightSetup():
    shared_vars.SPR_PIRATE = jtrukSpriteModel(SPR_PIRATE_MODEL_ID, "./ninja.png")  # ./goal.png "/pim-logo.png"
    if not shared_vars.SPR_PIRATE.load(gfx):
        return ["Pirate sprite not loaded - check the file is on the Picovision"]
    
    return None

def mainDemo():
    global T, SCRIPT, SCRIPT_ACTION_T, SCRIPT_ACTION_CAP, SCRIPT_ITEM, SCRIPT_POS, ILOOP
    global EFFECT
    TIMER_SAMPLES=10
    TIMER_N=0
    TIMER_COUNT=0
    DURATION=""
    LAST_PICOVISION_LINES=[]
    LAST_PICOVSION_LETTER=0
    shared_vars.MUSIC_IN_ACTION = "play"

    while True:
        timestamp=ticks_cpu()

        gfx.set_pen(BLACK)
        gfx.clear()

        SCRIPT_ACTION_T += 1
        if SCRIPT_ACTION_T>=SCRIPT_ACTION_CAP:
            if EFFECT != None:
                EFFECT.cleanup()

            SCRIPT_ACTION_T=0
            SCRIPT_POS += 1
            if SCRIPT_POS >= len(SCRIPT):
                SCRIPT_POS=0
                ILOOP += 1

            SCRIPT_ITEM=SCRIPT[SCRIPT_POS]
            SCRIPT_ACTION_CAP=('duration' in SCRIPT_ITEM) and SCRIPT_ITEM['duration'] or 50
        
        # End after two loops
        if ILOOP > 2:
            return

        lerpPos=SCRIPT_ACTION_T/SCRIPT_ACTION_CAP
        tweenPos=smoothStep(lerpPos)

        doScript(lerpPos, tweenPos)

        otherIntensity = rampUpThenDown(lerpPos)
        if SCRIPT_ITEM['action'] == "move":
            focusLetter = SCRIPT_ITEM['letter'] if lerpPos > .5 else (SCRIPT_ITEM['letter']-1)%len(PICOVISION.iLetterDef)
            LAST_PICOVISION_LINES = PICOVISION.draw(
                gfx, DISPLAY,
                None,
                [-CAM['p'][0],-CAM['p'][1],-CAM['p'][2]], [0,0,CAM['rz']],
                {
                    't': T,
                    'focusLetter': focusLetter,
                    'otherIntensity': otherIntensity
                }
            )
            LAST_PICOVSION_LETTER = SCRIPT_ITEM['letter']
        else:
            PICOVISION.drawLines(LAST_PICOVISION_LINES, gfx, LAST_PICOVSION_LETTER, LAST_PICOVSION_LETTER+1)

        gfx.set_pen(WHITE)
        gfx.text(DURATION, 0,0, fixed_width=1,scale=1)
        gfx.text(str(shared_vars.MUSIC_OUT_ROW), 30,100, fixed_width=1,scale=1)
        debugPrintScript()

        gfx.update()
        T=T+1

        TIMER_COUNT += ticks_cpu()-timestamp
        TIMER_N += 1
        if TIMER_N == TIMER_SAMPLES:
            DURATION=str(TIMER_COUNT/TIMER_SAMPLES)
            TIMER_N=0
            TIMER_COUNT=0

def textScreen(textLines, duration):
    t = 0
    while t < duration:
        gfx.set_pen(BLACK)
        gfx.clear()

        for i, line in enumerate(textLines):
            gfx.set_pen(gfx.create_pen_hsv(10+i*.01-t*.005, 1, 1))
            x, y = 30, i*10
            gfx.text(line, x,y, fixed_width=1,scale=1)

        gfx.update()
        t = t + 1

def raiseError(textLines):
    while True:
        gfx.set_pen(BLACK)
        gfx.clear()

        gfx.set_pen(RED)
        gfx.text("Software Failure (Guru Meditation)", 0,0, scale=1)
        for i, line in enumerate(textLines):
            gfx.text(line, 0,20+i*10, scale=1)

        gfx.update()

def demo_thread():
    errors = preflightSetup()
    if errors != None:
        raiseError(errors)

    """
    textScreen([
        "Welcome here",
        "This is my demo",
        "I hope you like it",
        "It's a bit rough around the edges",
        "But it's a demo",
        "So that's ok",
        "I hope you like it",
        "I hope you like it",
        "I hope you like it",
        "Welcome here",
        "This is my demo",
        "I hope you like it",
        "It's a bit rough around the edges",
        "But it's a demo",
        "So that's ok",
        "I hope you like it",
        "I hope you like it",
        "I hope you like it",
    ], 200)
    """

    mainDemo()

    textScreen([
        "End!",
    ], 200)

def sfx_thread():
    musicPlayer = MusicPlayer(main_tune)
    musicPlayer.play()

def peakAmbition():
    _thread.start_new_thread(demo_thread, ())
    sfx_thread()

peakAmbition()