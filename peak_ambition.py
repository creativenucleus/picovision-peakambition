from math import sin, cos, pi, atan2, sqrt, pow, fmod, floor
from picographics import PicoGraphics, PEN_RGB555
from time import ticks_cpu
import random
import _thread
from jtruk_music_player import MusicPlayer
from jtruk_3d import jtruk3DSetGfx, makeV, jtruk3DModelBoxLines, jtruk3DModelIcosahedron
from jtruk_3d_picovision import jtruk3DModelPicovision
from jtruk_effect_landscape import jtrukEffectLandscape
from jtruk_tune_main import tune as main_tune
import jtruk_thread_vars

gfx=PicoGraphics(pen_type=PEN_RGB555, width=320, height=240)
WIDTH,HEIGHT=gfx.get_bounds()
DISPLAY={'xmid': WIDTH/2, 'ymid': HEIGHT/2, 'scale': 100}
tau=pi*2
WHALF=int(WIDTH/2)
HHALF=int(HEIGHT/2)
BLACK=gfx.create_pen(0, 0, 0)
WHITE=gfx.create_pen(255, 255, 255)
RED=gfx.create_pen(255, 0, 0)
T=0

jtruk3DSetGfx(gfx)

box=jtruk3DModelBoxLines()
icosahedron=jtruk3DModelIcosahedron()
picovision=jtruk3DModelPicovision()
effectLandscape=jtrukEffectLandscape(6)

def effect1P(lerpPos, tweenPos):
    effectLandscape.draw(gfx, DISPLAY, None, None, None, T)

def effect2I(lerpPos, tweenPos):
    baseA=sin(lerpPos*10)*2
    for y in range(HEIGHT/3):
        yline=y*3
        a=baseA+y*0.01+sin(yline*.01+lerpPos*14)*2
        w=80*tweenPos
        xc=WHALF+sin(yline*.015+lerpPos*20)*40*lerpPos
        sina=sin(a)
        cosa=cos(a)
        x0=int(xc+sina*w)
        x1=int(xc+cosa*w)
        x2=int(xc-sina*w)
        x3=int(xc-cosa*w)
        cshift=lerpPos+y*.005

        if x1>x0:
            gfx.set_pen(gfx.create_pen_hsv(0+cshift,1,-sina*.5+.5))
            gfx.pixel_span(x0,yline,x1-x0)
        if x2>x1:
            gfx.set_pen(gfx.create_pen_hsv(0.25+cshift,1,-cosa*.5+.5))
            gfx.pixel_span(x1,yline,x2-x1)
        if x3>x2:
            gfx.set_pen(gfx.create_pen_hsv(0.5+cshift,1,sina*.5+.5))
            gfx.pixel_span(x2,yline,x3-x2)
        if x0>x3:
            gfx.set_pen(gfx.create_pen_hsv(0.75+cshift,1,cosa*.5+.5))
            gfx.pixel_span(x3,yline,x0-x3)

VARS_3C={
    'x': 0,
    'y': -1,
    'z': 0,
    'dx': .07,
    'dy': .01,
    'dz': .12,
    'rx': 0,
    'drx': .07,
    'rz': 0,
    'drz': .07,
    'vertices': [],
    'triangles': [],
}


def effect3C(lerpPos, tweenPos):
    global DISPLAY

    rX,rY,rZ=lerpPos*19,VARS_3C['rx'],VARS_3C['rz']
    VARS_3C['x']+=VARS_3C['dx']
    VARS_3C['y']+=VARS_3C['dy']
    VARS_3C['z']+=VARS_3C['dz']
    overY = VARS_3C['y']-1
    if overY > 0:
        VARS_3C['y']=1-(VARS_3C['dy']-overY)
        VARS_3C['dy']=-VARS_3C['dy']
    if VARS_3C['x'] < -3 or VARS_3C['x'] > 3:
        VARS_3C['dx']=-VARS_3C['dx']
        VARS_3C['drz']=-VARS_3C['drz']
    if VARS_3C['z'] < -1 or VARS_3C['z'] > 1:
        VARS_3C['dz']=-VARS_3C['dz']
        VARS_3C['drx']=-VARS_3C['drx']
    VARS_3C['dy']+=.02
    VARS_3C['rx']+=VARS_3C['drx']
    VARS_3C['rz']+=VARS_3C['drz']
    icosahedron.draw(gfx, DISPLAY, [rX, rY, rZ], [VARS_3C['x'],VARS_3C['y'],5+VARS_3C['z']], None, T)


def effect4O(lerpPos, tweenPos):
    for iD in range(10):
        d=pow(fmod(iD/10+T*.03, 1),2)
        for iA in range(10):
            a=iA/10*pi*2+iD*.2+T*.02
            gfx.set_pen(gfx.create_pen_hsv(iA*.1+iD*.2,1,d))
            x=int((sin(1/(iD+1)*T*.01)*d*50)+(sin(a)*d*180))
            y=int(cos(a)*d*140)
            gfx.circle(WHALF+x,HHALF+y,int(4*d))
            #gfx.pixel(WHALF+x,HHALF+y)

E5V_DOTS=[]
def effect5V(lerpPos, tweenPos):
    global E5V_DOTS
    if random.randint(0,10)==0:
        E5V_DOTS.append({'x': random.uniform(-1, 1), 'y': -1, 'dx': random.uniform(-.001,.001), 'dy': 0})
    gfx.set_pen(WHITE)
    for d in E5V_DOTS:
        d['dy'] += .0001
        d['x'] += d['dx']
        d['y'] += d['dy']
        if d['y']>=1:
            del d
        else:
            x=WHALF+int(d['x']*80)
            y=HHALF+int(d['y']*(HHALF+10))
            gfx.circle(x,y,4)

def effect6I(lerpPos, tweenPos):
    nBars=20
    for i in range(nBars):
        x=120+int(sin(i*.07+lerpPos*16)*40+sin(i*.12+lerpPos*25)*40)
        y=70+i*4
        gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,i/nBars))
        gfx.rectangle(x-4,y,8,HEIGHT-y)

def effect7S(lerpPos, tweenPos):
    nBobs=20
    for i in range(nBobs):
        x=WHALF+int(sin(i*.35+lerpPos*25)*120*lerpPos)
        y=HHALF+int(sin(i*.2+lerpPos*40)*80*lerpPos)
        gfx.set_pen(gfx.create_pen_hsv(i/nBobs,1,.6))
        gfx.circle(x-1,y-1,8)
        gfx.set_pen(gfx.create_pen_hsv(i/nBobs,.8,1))
        gfx.circle(x-4,y-4,3)

def effect8I(lerpPos, tweenPos):
    nBars=5
    for i in range(nBars):
        a=i*tau/(nBars)+sin(lerpPos*5)*3
        y=HHALF+int(sin(a)*60)
        for ya in range(10):
            gfx.set_pen(gfx.create_pen_hsv(i/nBars,1,ya/10))
            yline=y-ya+5
            gfx.pixel_span(0,yline,WIDTH)

SCRIPT=[
#    {'action':"effect", 'fn':effect1P, 'duration': 100, 'legend': "Wave Landscape", 'detail': ""},
    {'action':"move", 'letter':0, 'rz': -pi*.5},
    {'action':"move", 'letter':1, 'rz': pi},
    {'action':"effect", 'fn':effect2I, 'duration': 100, 'legend': "Twister", 'detail': "What an amazing effect\nDoes this spread over two lines?"},
    {'action':"move", 'letter':2, 'rz': -pi*.5},
    {'action':"effect", 'fn':effect3C, 'duration': 100, 'legend': "Icosahedron", 'detail': "With basic face lighting"},
    {'action':"move", 'letter':3, 'rz': -pi*1.25},
    {'action':"effect", 'fn':effect4O, 'duration': 100, 'legend': "Dot Tunnel", 'detail': ""},
    {'action':"move", 'letter':4, 'rz': 0},
    {'action':"effect", 'fn':effect5V, 'duration': 100, 'legend': "Bounces", 'detail': ""},
    {'action':"move", 'letter':5, 'rz': pi},
    {'action':"effect", 'fn':effect6I, 'duration': 100, 'legend': "Alcatraz bars", 'detail': ""},
    {'action':"move", 'letter':6, 'rz': -pi*.5},
    {'action':"effect", 'fn':effect7S, 'duration': 100, 'legend': "Bobs", 'detail': ""},
    {'action':"move", 'letter':7, 'rz': -pi*1.5},
    {'action':"effect", 'fn':effect8I, 'duration': 100, 'legend': "Raster bars", 'detail': ""},
    {'action':"move", 'letter':8, 'rz': -pi*1.75},
    {'action':"move", 'letter':9, 'rz': -pi*.25},
]
SCRIPT_POS=-1
SCRIPT_ACTION_CAP=50
SCRIPT_ACTION_T=SCRIPT_ACTION_CAP
SCRIPT_ITEM=None
CAM={'p': makeV(0,0,0), 'rz': 0}
CAM_TWEEN0={'p': makeV(0,0,0), 'rz': 0}
CAM_TWEEN1={'p': makeV(0,0,0), 'rz': 0}

# return lerpPos and tweenPos
def doScript():
    global SCRIPT, SCRIPT_POS, SCRIPT_ITEM, SCRIPT_ACTION_T, SCRIPT_ACTION_CAP
    global CAM, CAM_TWEEN0, CAM_TWEEN1
    global LETTERS
    SCRIPT_ACTION_T += 1
    if SCRIPT_ACTION_T>=SCRIPT_ACTION_CAP:
        SCRIPT_POS=(SCRIPT_POS+1)%len(SCRIPT)
        SCRIPT_ACTION_T=0
        SCRIPT_ITEM=SCRIPT[SCRIPT_POS]
        SCRIPT_ACTION_CAP=('duration' in SCRIPT_ITEM) and SCRIPT_ITEM['duration'] or 50
    
    lerpPos=SCRIPT_ACTION_T/SCRIPT_ACTION_CAP
    tweenPos=smoothStep(lerpPos)
    if SCRIPT_ITEM['action'] == "move":
        if SCRIPT_ACTION_T==0:
            CAM_TWEEN0=CAM
            letter=picovision.getLetterPos(SCRIPT_ITEM['letter'])
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
        SCRIPT_ITEM['fn'](lerpPos, tweenPos)
        if 'legend' in SCRIPT_ITEM:
            x,y=WHALF-len(SCRIPT_ITEM['legend'])*7,10
            xl,yl=20,HEIGHT-20
            gfx.set_pen(RED)
            gfx.text(SCRIPT_ITEM['legend'], x+1,y+1)
            gfx.set_pen(BLACK)
            gfx.text(SCRIPT_ITEM['detail'], xl+1,yl+1, scale=1)
            gfx.set_pen(WHITE)
            gfx.text(SCRIPT_ITEM['legend'], x,y)
            gfx.text(SCRIPT_ITEM['detail'], xl,yl, scale=1)
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

def mainDemo():
    TIMER_SAMPLES=10
    TIMER_N=0
    TIMER_COUNT=0
    DURATION=""
    LAST_PICOVISION_LINES=[]
    LAST_PICOVSION_LETTER=0
    global T
    jtruk_thread_vars.MUSIC_IN_ACTION = "play"
    while True:
        timestamp=ticks_cpu()

        gfx.set_pen(BLACK)
        gfx.clear()

        lerpPos, _ = doScript()
        otherIntensity = rampUpThenDown(lerpPos)
        if SCRIPT_ITEM['action'] == "move":
            focusLetter = SCRIPT_ITEM['letter'] if lerpPos > .5 else (SCRIPT_ITEM['letter']-1)%len(picovision.iLetterDef)
            LAST_PICOVISION_LINES = picovision.draw(
                gfx, DISPLAY,
                None,
                [-CAM['p'][0],-CAM['p'][1],-CAM['p'][2]], [0,0,CAM['rz']],
                T, {
                    'focusLetter': focusLetter,
                    'otherIntensity': otherIntensity
                }
            )
            LAST_PICOVSION_LETTER = SCRIPT_ITEM['letter']
        else:
            picovision.drawLines(LAST_PICOVISION_LINES, gfx, LAST_PICOVSION_LETTER, LAST_PICOVSION_LETTER+1)

        gfx.set_pen(WHITE)
        gfx.text(DURATION, 0,0, fixed_width=1,scale=1)
        gfx.text(str(jtruk_thread_vars.MUSIC_OUT_ROW), 30,100, fixed_width=1,scale=1)
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

def demo_thread():
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

    mainDemo()

def sfx_thread():
    musicPlayer = MusicPlayer(main_tune)
    musicPlayer.play()

def peakAmbition():
    _thread.start_new_thread(demo_thread, ())
    sfx_thread()

peakAmbition()