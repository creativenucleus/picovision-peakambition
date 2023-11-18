from picographics import PicoGraphics, PEN_RGB555
from math import sin, pi
from time import ticks_cpu
import _thread
from jtruk_music_player import MusicPlayer
from jtruk_3d_picovision import jtruk3DModelPicovision
from pa_tune_main import getTune
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
from jtruk_3d import makeV, clamp

gfx=PicoGraphics(pen_type=PEN_RGB555, width=320, height=240)

shared_vars.GFX = gfx

WIDTH,HEIGHT=gfx.get_bounds()
DISPLAY={'w': WIDTH, 'h': HEIGHT, 'xmid': int(WIDTH/2), 'ymid': int(HEIGHT/2), 'scale': 100}
tau=pi*2
WHALF=int(WIDTH/2)
HHALF=int(HEIGHT/2)
BLACK=gfx.create_pen(0, 0, 0)
WHITE=gfx.create_pen(255, 255, 255)
RED=gfx.create_pen(255, 0, 0)
T=0

SCRIPT=[
    {'action':"move", 'letter':0, 'rz': -pi*.5},
    {'action':"effect", 'ceffect':paCEffect1P, 'duration': 2},
    {'action':"move", 'letter':1, 'rz': pi},
    {'action':"effect", 'ceffect':paCEffect2I, 'duration': 2},
    {'action':"move", 'letter':2, 'rz': -pi*.5},
    {'action':"effect", 'ceffect':paCEffect3C, 'duration': 2},
    {'action':"move", 'letter':3, 'rz': -pi*1.25},
    {'action':"effect", 'ceffect':paCEffect4O, 'duration': 2},
    {'action':"move", 'letter':4, 'rz': 0},
    {'action':"effect", 'ceffect':paCEffect5V, 'duration': 2},
    {'action':"move", 'letter':5, 'rz': pi},
    {'action':"effect", 'ceffect':paCEffect6I, 'duration': 2},
    {'action':"move", 'letter':6, 'rz': -pi*.5},
    {'action':"effect", 'ceffect':paCEffect7S, 'duration': 2},
    {'action':"move", 'letter':7, 'rz': -pi*1.5},
    {'action':"effect", 'ceffect':paCEffect8I, 'duration': 2},
    {'action':"move", 'letter':8, 'rz': -pi*1.75},
    {'action':"effect", 'ceffect':paCEffect9O, 'duration': 2},
    {'action':"move", 'letter':9, 'rz': -pi*.25},
    {'action':"effect", 'ceffect':paCEffect10N, 'duration': 2},
]

def getPatternDuration(iScriptItem):
    return (SCRIPT[iScriptItem]['duration']) if ('duration' in SCRIPT[iScriptItem]) else 2

ILOOP=0
SCRIPT_POS=0
CAM={'p': makeV(0,0, shared_vars.DISTANCE_START), 'rz': 0}
CAM_TWEEN0={'p': makeV(0,0,0), 'rz': 0}
CAM_TWEEN1={'p': makeV(0,0,0), 'rz': 0}
EFFECT=None
PICOVISION=jtruk3DModelPicovision()

def doScript(scriptItem, isInit, lerpPos, sweepPos):
    global CAM, CAM_TWEEN0, CAM_TWEEN1
    global EFFECT
    if scriptItem['action'] == "move":
        if isInit:
            CAM_TWEEN0=CAM
            letter=PICOVISION.getLetterPos(scriptItem['letter'])
            CAM_TWEEN1={'p': makeV(letter[0], letter[1], letter[2] + shared_vars.DISTANCE_CLOSE), 'rz': scriptItem['rz']}
        
        CAM={
            'p': makeV(
                lerp(sweepPos, CAM_TWEEN0['p'][0], CAM_TWEEN1['p'][0]) + sin(sweepPos*pi*2) * 4,
                lerp(sweepPos, CAM_TWEEN0['p'][1], CAM_TWEEN1['p'][1]) + sin(sweepPos*pi*4) * 2,
                lerp(sweepPos, CAM_TWEEN0['p'][2], CAM_TWEEN1['p'][2]) + sin(sweepPos*pi) * shared_vars.DISTANCE_FAR
            ),
            'rz': lerp(sweepPos, CAM_TWEEN0['rz'], CAM_TWEEN1['rz'])
        }
    elif scriptItem['action'] == "effect":
        if isInit:
            EFFECT=scriptItem['ceffect'](ILOOP)

        EFFECT.draw(gfx, DISPLAY, lerpPos, sweepPos)
        
        if ILOOP == 1:
            legend = EFFECT.legend()
            detail = EFFECT.detail()
            x,y=5,190
            gfx.set_pen(RED)
            gfx.text(legend, x+1,y+1, scale=1)
            gfx.set_pen(WHITE)
            gfx.text(legend, x,y, scale=1)
            gfx.set_pen(BLACK)
            gfx.text(detail, x+1,y+15, scale=1)
            gfx.set_pen(WHITE)
            gfx.text(detail, x,y+14, scale=1)

def lerp(t,v1,v2):
    return (1-t)*v1+t*v2

def smoothStep(t):
    return t * t * (3.0 - 2.0 * t)

# t is the unit 0-1, rs is rampSpeed (e.g. 0.1)
def rampUpThenDown(t, rs):
    if t<rs:
        return t/rs
    elif t>(1-rs):
        return (1-t)/rs
    else:
        return 1

def preflightSetup():
    #shared_vars.SPR_PIRATE = jtrukSpriteModel(SPR_PIRATE_MODEL_ID, "./ninja.png")  # ./goal.png "/pim-logo.png"
    #if not shared_vars.SPR_PIRATE.load(gfx):
    #    return ["Pirate sprite not loaded - check the file is on the Picovision"]
    
    return None

def mainDemo():
    global T, SCRIPT, SCRIPT_POS, ILOOP
    global EFFECT, CAM
    TIMER_SAMPLES=10
    TIMER_N=0
    TIMER_COUNT=0
    # DURATION=""
    LAST_PICOVISION_LINES=[]
    LAST_PICOVSION_LETTER=0
    scriptItem = SCRIPT[SCRIPT_POS]
    startPattern = 0
    patternDuration = getPatternDuration(0)
    nextMusicPatternTrigger = patternDuration
    isEffectInit = True
    shared_vars.MUSIC_IN_ACTION = "play"
    focusLetter = 9
    cueStartNextScriptItem = False

    # Use this code for testing effects in isolation...
    # paCEffect1P - landscape
    # paCEffect2I - twister
    # paCEffect3C - filled model
    # paCEffect4O - dot tunnel
    # paCEffect5V - V
    # paCEffect6I - alcatraz bars
    # paCEffect7S - bobs
    # paCEffect8I - raster bars
    # paCEffect9O - starfield
    # paCEffect10N - picovision
    """
    effect = paCEffect3C(1)
    while True:
        gfx.set_pen(BLACK)
        gfx.clear()

        musicAccPattern = shared_vars.MUSIC_OUT_ACCPATTERN 
        musicRow = shared_vars.MUSIC_OUT_ROW
        patternDuration = 4
        lerpPos = ((musicAccPattern - startPattern) * 64 + musicRow) / (patternDuration * 64)
        sweepPos = smoothStep(lerpPos)
        effect.draw(gfx, DISPLAY, lerpPos, sweepPos)
        gfx.update()
        T=T+1
    """
    while True:
        timestamp=ticks_cpu()

        gfx.set_pen(BLACK)
        gfx.clear()

        musicAccPattern = shared_vars.MUSIC_OUT_ACCPATTERN 
        musicRow = shared_vars.MUSIC_OUT_ROW

        if cueStartNextScriptItem:
            isEffectInit = True
            if EFFECT != None:
                EFFECT.cleanup()

            SCRIPT_POS += 1
            if SCRIPT_POS >= len(SCRIPT):
                SCRIPT_POS=0
                CAM={'p': makeV(0,0, shared_vars.DISTANCE_START), 'rz': 0}
                ILOOP += 1

            startPattern = musicAccPattern
            patternDuration = getPatternDuration(SCRIPT_POS)
            nextMusicPatternTrigger += patternDuration
            scriptItem = SCRIPT[SCRIPT_POS]
            cueStartNextScriptItem = False

            lerpPos = ((musicAccPattern - startPattern) * 64 + musicRow) / (patternDuration * 64)
            sweepPos = smoothStep(lerpPos)

            # End after two loops
            if ILOOP >= 2:
                return
        else:
            # Check if our music pattern has changed
            if musicAccPattern >= nextMusicPatternTrigger:
                # Do one last final from the current effect (make sure all end at pos = 1)
                lerpPos = 1
                sweepPos = 1
                cueStartNextScriptItem = True
            else:
                lerpPos = ((musicAccPattern - startPattern) * 64 + musicRow) / (patternDuration * 64)
                sweepPos = smoothStep(lerpPos)

        intensityRamp = rampUpThenDown(lerpPos, .2)
        intensityRamp2 = rampUpThenDown(lerpPos, .1)

        # Draw the stored shape...
        if scriptItem['action'] == "effect":
            if focusLetter == 9:
                PICOVISION.drawLines(LAST_PICOVISION_LINES, gfx, LAST_PICOVSION_LETTER, LAST_PICOVSION_LETTER+1, clamp(1 - lerpPos * 10, 0, 1))
            else:
                PICOVISION.drawLines(LAST_PICOVISION_LINES, gfx, LAST_PICOVSION_LETTER, LAST_PICOVSION_LETTER+1, .2+(1-intensityRamp2)*.8)


        doScript(scriptItem, isEffectInit, lerpPos, sweepPos)

        if scriptItem['action'] == "move":
            if lerpPos > .5:
                focusLetter = scriptItem['letter']
            if scriptItem['letter'] == 0 and lerpPos < .5:
                intensityRamp = 1  # Special case for wraparound

            LAST_PICOVISION_LINES = PICOVISION.draw(
                gfx, DISPLAY,
                [sin(sweepPos*pi*2)*3+sin(lerpPos*pi*4),0,0],
                [-CAM['p'][0],-CAM['p'][1],-CAM['p'][2]],
                [0,0,CAM['rz']],
                extra={
                    't': T,
                    'focusLetter': focusLetter,
                    'otherIntensity': intensityRamp
                }
            )
            LAST_PICOVSION_LETTER = scriptItem['letter']

        """
        gfx.set_pen(WHITE)
        gfx.text(DURATION, 0,10, fixed_width=1,scale=1)
        gfx.text("{}".format(lerpPos), 0, 20, fixed_width=1,scale=1)
        """

        gfx.update()
        T=T+1

        TIMER_COUNT += ticks_cpu()-timestamp
        TIMER_N += 1
        if TIMER_N == TIMER_SAMPLES:
            DURATION=str(TIMER_COUNT/TIMER_SAMPLES)
            TIMER_N=0
            TIMER_COUNT=0

        isEffectInit = False

        
def textScreen(textLines, pvIsMoveIn, preWait, animDuration, postWait):
    t = 0
    while True:
        gfx.set_pen(BLACK)
        gfx.clear()

        draw = False
        z = 0
        unitT = clamp((t - preWait) / animDuration, 0, 1)

        if pvIsMoveIn:
            if unitT > 0:
                draw = True
                z = (1 - unitT) * -9
        else:
            if unitT < 1:
                draw = True
                z = unitT * -9

        if draw:
            PICOVISION.draw(
                gfx, DISPLAY,
                None,
                [-CAM['p'][0],-CAM['p'][1],-CAM['p'][2] + z],
                None,
                extra={
                    't': T,
                    'focusLetter': 9,
                    'otherIntensity': 1
                }
            )

        yText = 0
        for line in textLines:
            yText += 12 + line['ys']
            scale = 1 if not "scale" in line else line["scale"]
            h = 10+yText*.001-t*.005
            gfx.set_pen(gfx.create_pen_hsv(h+.3, 1, .5))
            gfx.text(line['l'], line['x']+1+int(sin(1+t*.08+yText)), yText+int(sin(t*.06+yText)), fixed_width=1,scale=scale)
            gfx.set_pen(gfx.create_pen_hsv(h, .7, 1))
            gfx.text(line['l'], line['x'], yText, fixed_width=1,scale=scale)

        gfx.update()
        t = t + 1
        if t > preWait + animDuration + postWait:
            return

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

    textScreen([
        {'ys': 10, 'x': 90, 'l': "Aiming Higher than you dare", },
        {'ys': 10, 'x': 10, 'l': "Putting More on your plate than you think you can handle"},
        {'ys': 10, 'x': 75, 'l': "There's nothing finer than a little"},
        {'ys': 90, 'x': 76, 'l': "- PEAK AMBITION -", 'scale': 2},
        {'ys': 40, 'x': 75, 'l': "jtruk / Pimoroni Picovision / 2023"},
    ], True, 150, 100, 50)

    mainDemo()

    textScreen([
        {'ys': 10, 'x': 116, 'l': "I hope you enjoyed"},
        {'ys': 14, 'x': 76, 'l': "- PEAK AMBITION -", 'scale':2},
        {'ys': 110, 'x': 20, 'l': "Greetz to all, esp: RiFT, Field-FX & the Byte Jam crowd!"},
        {'ys': 6, 'x': 3, 'l': "Thanks to the Picovision, the Pimoroni folks, and sin + cos <3"},
        {'ys': 6, 'x': 90, 'l': "See you in another demo... :)"},
        {'ys': 12, 'x': 75, 'l': "jtruk / Pimoroni Picovision / 2023"},
    ], False, 50, 100, 50)

    shared_vars.MUSIC_IN_ACTION = "stop"

def sfx_thread():
    musicPlayer = MusicPlayer(getTune())
    musicPlayer.play()

def peakAmbition():
    _thread.start_new_thread(demo_thread, ())
    sfx_thread()

peakAmbition()