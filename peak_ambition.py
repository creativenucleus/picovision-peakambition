from math import sin, cos, pi, atan2, sqrt, pow, fmod, floor
from picographics import PicoGraphics, PEN_RGB555
from time import ticks_cpu
import random
import _thread
from jtruk_music_player import MusicPlayer
from jtruk_3d import jtruk3DModelBoxLines, jtruk3DSetGfx

gfx=PicoGraphics(pen_type=PEN_RGB555, width=320, height=240)
WIDTH,HEIGHT=gfx.get_bounds()
tau=pi*2
WHALF=int(WIDTH/2)
HHALF=int(HEIGHT/2)
BLACK=gfx.create_pen(0, 0, 0)
WHITE=gfx.create_pen(255, 255, 255)
RED=gfx.create_pen(255, 0, 0)
T=0

jtruk3DSetGfx(gfx)

box=jtruk3DModelBoxLines()

def clamp(v,min,max):
    if v<=min:
        return min
    if v>=max:
        return max
    return v    

def makeP(x, y, z):
    return {'x': x, 'y': y, 'z': z}

def rotX(p,a):
    return {'x':p['x'], 'y':p['y']*cos(a)-p['z']*sin(a), 'z':p['y']*sin(a)+p['z']*cos(a)}

def rotY(p,a):
    return {'x': p['x']*cos(a)-p['z']*sin(a), 'y':p['y'], 'z':p['x']*sin(a)+p['z']*cos(a)}

def rotZ(p,a):
    return {'x': p['x']*cos(a)-p['y']*sin(a), 'y':p['x']*sin(a)+p['y']*cos(a), 'z':p['z']}

def trans(p,x,y,z):
    return {'x': p['x']+x, 'y': p['y']+y, 'z': p['z']+z}

# Translate in place
def transM(points, x,y,z):
    for p in points:
        p['x'] += x
        p['y'] += y
        p['z'] += z
    return points

# Scale in place...
def scaleM(points,sX,sY,sZ):
    for p in points:
        p['x'] *= sX
        p['y'] *= sY
        p['z'] *= sZ
    return points

def project(p):
    zF=7-p['z']/1.5
    return [floor(WHALF+(p['x']/zF)*100),floor(HHALF+(p['y']/zF)*(WHALF/HHALF)*100),p['z']/zF]

def makeLetter(letter):
    if letter=='P':
        return (
            [makeP(-1,1,0), makeP(-1,-1,0), makeP(0,-1,0)] +
            transM(scaleM(getPointsArc(8,pi*2.5,pi*1.5),1,.5,1),0,-.5,0) +
            [makeP(-1,0,0)]
        )
    elif letter=='I':
        return [makeP(0,-1,0),makeP(0,1,0)]
    elif letter=='C':
        return getPointsArc(12,pi*.25,pi*2-pi*.25)
    elif letter=='O':
        return getPointsArc(16,0,pi*2)
    elif letter=='V':
        return [makeP(-1,-1,0),makeP(0,1,0),makeP(1,-1,0)]
    if letter=='S':
        return (
            transM(scaleM(getPointsArc(8,0,pi*1.5),1,.5,1),0,-.5,0) +
            transM(scaleM(getPointsArc(8,pi*.5,-pi*1),1,.5,1),0,.5,0)
        )
    elif letter=='N':
        return [makeP(-1,1,0),makeP(-1,-1,0),makeP(1,1,0),makeP(1,-1,0)]

def getPointsArc(nPoints,a0,a1):
    points=[]
    for a in range(nPoints+1):
        a=a0+(a/(nPoints))*(a1-a0)
        x=cos(a)
        y=-sin(a)
        points.append(makeP(x,y,0))
    return points
    

def drawLineString(points):
    global CAM
    for i,p in enumerate(points):
        p={'x': p['x']-CAM['x'], 'y': p['y']-CAM['y'], 'z': p['z']-CAM['z']}
        pProj=project(rotZ(rotX(p,sin(T*0.08)), sin(T*0.07)*.2))
        if i>0:
            gfx.line(pProj[0],pProj[1],pProjLast[0],pProjLast[1],2)
        pProjLast=pProj

LETTERS=[
    transM(makeLetter('P'), 0, 0, 0),
    transM(makeLetter('I'), 1.5, 0, 0),
    transM(makeLetter('C'), 3, 0, 0),
    transM(makeLetter('O'), 5, 0, 0),
    transM(makeLetter('V'), 7, 0, 0),
    transM(makeLetter('I'), 8.5, 0, 0),
    transM(makeLetter('S'), 10, 0, 0),
    transM(makeLetter('I'), 11.5, 0, 0),
    transM(makeLetter('O'), 13, 0, 0),
    transM(makeLetter('N'), 15.5, 0, 0),
]

for l in LETTERS:
    transM(l, 7.78, 0, 0)

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

def getNormal(p1,p2,p3):
    vecA={'x': p2['x']-p1['x'], 'y': p2['y']-p1['y'], 'z': p2['z']-p1['z']}
    vecB={'x': p3['x']-p1['x'], 'y': p3['y']-p1['y'], 'z': p3['z']-p1['z']}
    return {
        'x': vecA['y'] * vecB['z'] - vecA['z'] * vecB['y'],
        'y': vecA['z'] * vecB['x'] - vecA['x'] * vecB['z'],
        'z': vecA['x'] * vecB['y'] - vecA['y'] * vecB['x']
    }

def getDotProduct(v1,v2):
    return v1['x']*v2['x'] + v1['y']*v2['y'] + v1['z']*v2['z']

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

xp=.52573
zp=.85065
np=0        
VARS_3C['vertices']=[
    makeP(-xp,np,zp), makeP(xp,np,zp), makeP(-xp,np,-zp), makeP(xp,np,-zp),
    makeP(np,zp,xp), makeP(np,zp,-xp), makeP(np,-zp,xp), makeP(np,-zp,-xp),
    makeP(zp,xp,np), makeP(-zp,xp,np), makeP(zp,-xp,np), makeP(-zp,-xp,np)
]
     
VARS_3C['triangles']=[
    [0,4,1], [0,9,4], [9,5,4], [4,5,8], [4,8,1],
    [8,10,1], [8,3,10], [5,3,8], [5,2,3], [2,7,3],
    [7,10,3], [7,6,10], [7,11,6], [11,0,6], [0,1,6],
    [6,1,10], [9,0,11], [9,11,2], [9,2,5], [7,2,11]
]

def effect3C(lerpPos, tweenPos):
    tverts=[]
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
    VARS_3C['dy']+=.01
    VARS_3C['rx']+=VARS_3C['drx']
    VARS_3C['rz']+=VARS_3C['drz']

    for nvert,vert in enumerate(VARS_3C['vertices']):
        movedP = trans(rotZ(rotY(rotX(vert,rX),rY),rZ),VARS_3C['x'],VARS_3C['y'],5+VARS_3C['z'])
        tverts.append({
            'p': movedP,
            'pp': project(movedP)
        })
        
    lightVector={'x': 0, 'y': 0.77, 'z': 0.77}
    
    for ntri,tri in enumerate(VARS_3C['triangles']):
        p1,p2,p3=tverts[tri[0]], tverts[tri[1]], tverts[tri[2]]
        normal=getNormal(p1['p'],p2['p'],p3['p'])
        culling=getDotProduct(normal,{'x': 0, 'y': 0, 'z': 1})
        if culling>=0:
            lightStrength=clamp(getDotProduct(normal,lightVector)*.7,0,1)
            gfx.set_pen(gfx.create_pen_hsv(ntri/len(VARS_3C['triangles']),1,clamp(lightStrength*p2['pp'][2]/2,0,1)))
            gfx.triangle(p1['pp'][0],p1['pp'][1], p2['pp'][0],p2['pp'][1], p3['pp'][0],p3['pp'][1])

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
    {'action':"effect", 'fn':effect3C, 'duration': 200, 'legend': "Icosahedron", 'detail': "With basic face lighting"},
    {'action':"effect", 'fn':effect4O, 'duration': 200, 'legend': "Dot Tunnel", 'detail': ""},
    {'action':"effect", 'fn':effect7S, 'duration': 200, 'legend': "Bobs", 'detail': ""},
    {
        'action':"effect", 'fn':effect2I, 'duration': 200, 'legend': "Twister",
        'detail': "What an amazing effect\nDoes this spread over two lines?"
    },
    {'action':"move", 'letter':0},
#    {'action':"effect", 'fn':effect5V, 'duration': 400, 'legend': "Bounces", 'detail': ""},
    {'action':"move", 'letter':1},
    {'action':"move", 'letter':3},
    {'action':"move", 'letter':4},
    {'action':"move", 'letter':5},
    {'action':"effect", 'fn':effect6I, 'duration': 200, 'legend': "Alcatraz bars", 'detail': ""},
    {'action':"move", 'letter':6},
    {'action':"move", 'letter':7},
    {'action':"effect", 'fn':effect8I, 'duration': 200, 'legend': "Raster bars", 'detail': ""},
    {'action':"move", 'letter':8},
    {'action':"move", 'letter':9},
]
SCRIPT_POS=-1
SCRIPT_ACTION_CAP=50
SCRIPT_ACTION_T=SCRIPT_ACTION_CAP
SCRIPT_ITEM=None
CAM=makeP(0,0,0)
CAM_TWEEN0=makeP(0,0,0)
CAM_TWEEN1=makeP(0,0,0)

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
            letter=LETTERS[SCRIPT_ITEM['letter']]
            CAM_TWEEN1={'x':letter[0]['x'], 'y':0, 'z':0}
        CAM=makeP(
            lerp(tweenPos, CAM_TWEEN0['x'], CAM_TWEEN1['x']),
            lerp(tweenPos, CAM_TWEEN0['y'], CAM_TWEEN1['y']),
            lerp(tweenPos, CAM_TWEEN0['z'], CAM_TWEEN1['z'])
        )
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
        

def debugPrintScript():
    global SCRIPT_POS, SCRIPT_ACTION_T
    gfx.text("POS {} T {}".format(SCRIPT_POS, SCRIPT_ACTION_T), 0,10, fixed_width=1,scale=1)
    
def lerp(t,v1,v2):
    return (1-t)*v1+t*v2

def smoothStep(t):
    return t * t * (3.0 - 2.0 * t)
    
def gfx_thread():
    TIMER_SAMPLES=10
    TIMER_N=0
    TIMER_COUNT=0
    DURATION=""
    global T
    display={'xmid': WIDTH/2, 'ymid': HEIGHT/2, 'scale': 100}
    while True:
        timestamp=ticks_cpu()

        gfx.set_pen(BLACK)
        gfx.clear()

        for i in range(16):
            x=4*(i%4)-6
            y=4*(i//4)-6
            trans=[x, y, 0]
            box.draw(display, [sin(i+T/30),cos(T/40),sin(i+T/50)], trans, None)
        
        """
        doScript()

        if SCRIPT_ITEM['action'] == "move":
            for i,letter in enumerate(LETTERS):
                gfx.set_pen(gfx.create_pen_hsv(i*0.02+T*0.01,1,1))
                drawLineString(letter)
        """

        gfx.set_pen(WHITE)
        gfx.text(DURATION, 0,0, fixed_width=1,scale=1)
        debugPrintScript()

        gfx.update()
        T=T+1

        TIMER_COUNT += ticks_cpu()-timestamp
        TIMER_N += 1
        if TIMER_N == TIMER_SAMPLES:
            DURATION=str(TIMER_COUNT/TIMER_SAMPLES)
            TIMER_N=0
            TIMER_COUNT=0

gfx_thread()

#_thread.start_new_thread(gfx_thread, ())

#musicPlayer = MusicPlayer()
#musicPlayer.run(0.06)

