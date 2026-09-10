from pathlib import Path
from html import escape
from functools import lru_cache
import math

OUT = Path(__file__).resolve().parent
W,H = 1600,900
BLACK='#111111'; MID='#60656b'; LIGHT='#f2f3f4'; GRID='#d6dadd'; WHITE='#ffffff'


def t(x,y,s,size=24,weight='normal',anchor='start',fill=BLACK,italic=False):
    st='font-style:italic;' if italic else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" style="{st}">{escape(str(s))}</text>'

def multiline(x,y,lines,size=22,weight='normal',anchor='middle',fill=BLACK,dy=1.25):
    out=[f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">']
    for i,line in enumerate(lines):
        shift=0 if i==0 else size*dy
        out.append(f'<tspan x="{x}" dy="{shift if i else 0}">{escape(str(line))}</tspan>')
    out.append('</text>')
    return ''.join(out)

def rect(x,y,w,h,fill=WHITE,stroke=BLACK,rx=10,sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def circle(cx,cy,r,fill=LIGHT,stroke=BLACK,sw=2):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def line(x1,y1,x2,y2,stroke=BLACK,sw=2,dash=None,arrow=False):
    da=f' stroke-dasharray="{dash}"' if dash else ''
    me=' marker-end="url(#arrow)"' if arrow else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{da}{me}/>'

def poly(points,stroke=BLACK,sw=3,dash=None,fill='none'):
    da=f' stroke-dasharray="{dash}"' if dash else ''
    pts=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    return f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}/>'

def base(title, subtitle=None):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>',
           '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#111111"/></marker></defs>',
           '<style>text{font-family:Arial,Helvetica,sans-serif}</style>',
           t(50,55,title,34,'bold')]
    if subtitle: parts.append(t(50,88,subtitle,20,'normal','start',MID))
    return parts

def finish(parts,name):
    parts.append('</svg>')
    (OUT/name).write_text('\n'.join(parts),encoding='utf-8')


def figure1():
    p=base('One ecological state space generates both reward amplitude and recurrence')
    p += [t(45,110,'A',28,'bold'),t(85,110,'Contingent sensing can avoid fixed cue burden',25,'bold'),
          t(905,110,'B',28,'bold'),t(945,110,'The same ecological states determine recurrence',25,'bold')]
    p += [circle(215,230,55),t(215,238,'coarse cue',20,'bold','middle')]
    p += [line(195,282,120,380,arrow=True),line(235,282,330,380,arrow=True),
          t(80,350,'A branch',16,'normal','start',MID),t(285,350,'B branch',16,'normal','start',MID)]
    for cx,label in [(105,'fine cue A'),(330,'fine cue B')]:
        p += [circle(cx,430,55),t(cx,423,label,18,'bold','middle'),t(cx,448,'A1 vs A2' if cx==105 else 'B1 vs B2',18,'bold','middle')]
    leafs=[(35,'A1'),(140,'A2'),(260,'B1'),(365,'B2')]
    for x,label in leafs:
        p += [rect(x,535,75,48,LIGHT),t(x+37.5,566,label,18,'bold','middle')]
    p += [line(82,482,73,535,arrow=True),line(128,482,177,535,arrow=True),line(307,482,297,535,arrow=True),line(352,482,402,535,arrow=True)]
    p += [rect(25,620,365,105),t(207,654,'Adaptive path',22,'bold','middle'),t(207,685,'coarse cue + relevant fine cue',19,'normal','middle',MID),t(207,715,'C_A = 2',19,'normal','middle',MID),
          rect(430,620,365,105),t(612,654,'Fixed cue set',22,'bold','middle'),t(612,685,'must cover all branches',19,'normal','middle',MID),t(612,715,'C_F = 3',19,'normal','middle',MID),
          t(410,610,'compare',15,'normal','middle',MID),line(390,605,430,605,arrow=True),
          rect(195,745,430,72,LIGHT),t(410,775,'structural gap  g = C_F − C_A = 1',21,'bold','middle'),t(410,803,'avoidable fixed burden under contingent sensing',17,'normal','middle',MID)]
    states=[(1080,255,'state 1'),(1340,230,'state 2'),(1450,485,'state 3'),(1165,535,'state 4')]
    for x,y,lbl in states:
        p += [circle(x,y,62),t(x,y+8,lbl,20,'bold','middle')]
    edges=[((1142,250),(1278,235)),((1370,285),(1422,420)),((1388,500),(1225,530)),((1137,475),(1095,318)),((1125,292),(1397,445)),((1305,285),(1200,478))]
    for a,b in edges: p.append(line(*a,*b,stroke=MID,sw=2,arrow=True))
    p += [t(1280,400,'transition operator P',22,'bold','middle'),line(1280,598,1280,655,arrow=True),
          rect(950,660,585,125,WHITE),t(1242,695,'Shared downstream state coordinates',22,'bold','middle'),
          t(1242,730,'finite sensing structure → g_i → s_i = λg_i − κ',19,'normal','middle',MID),
          t(1242,760,'state transitions P → recurrence of the same s_i',19,'normal','middle',MID),
          t(800,865,'Natural history declares alternatives, cues and distinctions; theory constrains the dynamics they can support.',22,'bold','middle')]
    finish(p,'figure1_state_space.svg')


def h_star(q,b):
    h=1
    while (b**h-1)/(b-1)-h < q: h+=1
    return h


@lru_cache(None)
def bounded_tree_internal_capacity(world_count, depth, max_arity):
    """Independent stdlib reproduction of the exact F_b(n,h) recurrence."""
    if world_count <= 1 or depth == 0:
        return 0
    best = 0
    for child_count in range(2, min(max_arity, world_count) + 1):
        dp = {(0, 0): 0}
        for used_children in range(child_count):
            nxt = {}
            remaining_children = child_count - used_children - 1
            for (_, used_budget), score in dp.items():
                max_budget = world_count - used_budget - remaining_children
                for child_budget in range(1, max_budget + 1):
                    key = (used_children + 1, used_budget + child_budget)
                    value = score + bounded_tree_internal_capacity(child_budget, depth - 1, max_arity)
                    if value > nxt.get(key, -1):
                        nxt[key] = value
            dp = nxt
        child_best = max(score for (used, budget), score in dp.items() if used == child_count and budget <= world_count)
        best = max(best, 1 + child_best)
    return best


def minimum_worlds_for_internal_count(internal_count, depth, max_arity):
    upper = 1 + (max_arity - 1) * internal_count
    for n in range(2, upper + 1):
        if bounded_tree_internal_capacity(n, depth, max_arity) >= internal_count:
            return n
    raise ArithmeticError('finite bounded-arity search unexpectedly failed')


def pareto_fixture(required_gap, max_arity):
    points = []
    best_worlds = None
    for h in range(h_star(required_gap, max_arity), h_star(required_gap, 2) + 1):
        fixed = h + required_gap
        n = minimum_worlds_for_internal_count(fixed, h, max_arity)
        if best_worlds is None or n < best_worlds:
            points.append((n, fixed, fixed, h))
            best_worlds = n
    return points


def figure2():
    p=base('Principal reachability result: from a required local regime back to finite sensing structure')
    xs=[50,420,790,1160]; titles=['local response','required phase','integer gap','finite structure']; subs=['(α, φ, a, b)','e.g. stable oscillation','q_osc','Pareto set P_b(q)']
    for i,x in enumerate(xs):
        p += [rect(x,95,310,95,LIGHT),t(x+155,132,titles[i],22,'bold','middle'),t(x+155,165,subs[i],19,'normal','middle',MID)]
        if i<3: p.append(line(x+310,143,xs[i+1]-10,143,arrow=True))
    p += [t(55,265,'A',28,'bold'),t(95,265,'Binary exact corner',25,'bold'),t(575,265,'B',28,'bold'),t(615,265,'Bounded arity: Pareto trade-off',25,'bold'),t(1080,265,'C',28,'bold'),t(1120,265,'Arity changes cue burden',25,'bold')]
    p += [rect(70,335,420,175,WHITE),t(280,380,'q = 2,  b = 2',22,'normal','middle'),t(280,415,'h₂*(2) = 3',21,'normal','middle',MID),t(280,450,'(n*, m*, E*) = (6, 5, 5)',21,'normal','middle',MID),t(280,485,'one exact componentwise corner',19,'normal','middle',MID),t(280,550,'required structure',20,'bold','middle'),line(115,570,445,570,arrow=True)]
    labs=[(85,'alternatives n','6'),(235,'cues m','5'),(385,'obligations E','5')]
    for x,l,v in labs: p += [rect(x,615,125,90,LIGHT),t(x+62,649,l,17,'bold','middle'),t(x+62,684,v,19,'normal','middle',MID)]
    x0,y0,x1,y1=610,720,1000,330
    p += [line(x0,y0,x0,y1),line(x0,y0,x1,y0),t(805,770,'represented alternatives n',18,'normal','middle'),t(570,520,'cue / obligation burden',18,'normal','middle')]
    for xv,px in [(7,720),(8,900)]: p += [line(px,720,px,728),t(px,750,str(xv),16,'normal','middle')]
    for yv,py in [(5,650),(6,455)]: p += [line(602,py,610,py),t(590,py+6,str(yv),16,'normal','end')]
    p += [circle(720,455,10,BLACK,BLACK),circle(900,650,10,BLACK,BLACK),line(728,463,892,642,stroke=MID,sw=2,dash='7 6'),t(740,435,'(7,6,6)',18,'bold'),t(912,632,'(8,5,5)',18,'bold'),t(805,350,'q = 3, b = 4',20,'bold','middle'),t(805,705,'Neither point dominates the other.',17,'bold','middle')]
    cx0,cy0,cx1,cy1=1130,720,1510,330
    p += [line(cx0,cy0,cx0,cy1),line(cx0,cy0,cx1,cy0),t(1320,770,'maximum cue arity b',18,'normal','middle'),t(1090,520,'minimum count',18,'normal','middle'),t(1350,365,'example: q = 2',20,'bold','middle')]
    def xp(b): return cx0+(b-2)/(6-2)*(cx1-cx0)
    def yp(v): return cy0-(v-3)/(8-3)*(cy0-cy1)
    for b in range(2,7): p += [line(xp(b),cy0,xp(b),cy0+8),t(xp(b),748,str(b),16,'normal','middle')]
    for v in range(3,9): p += [line(cx0-8,yp(v),cx0,yp(v)),t(cx0-15,yp(v)+6,str(v),16,'normal','end')]
    npts=[(xp(b),yp(6)) for b in range(2,7)]; mvals=[5,4,4,4,4]; mpts=[(xp(b),yp(v)) for b,v in zip(range(2,7),mvals)]
    p += [poly(npts,BLACK,3),poly(mpts,MID,3,'9 7'),t(1415,yp(6)-15,'n_min = 6',18,'bold','middle'),t(1360,yp(6)+28,'represented alternatives',15,'normal','middle',MID),t(1340,yp(4)+28,'m_min = E_min',18,'normal','middle',MID),t(1420,yp(4)-12,'cues / obligations',15,'normal','middle',MID)]
    p += [rect(55,810,1490,65,LIGHT),t(800,838,'Interpretation: richer cue outcomes can reduce routing burden without reducing the alternatives that must be represented.',20,'bold','middle'),t(800,865,'Finite structural counts, not Shannon-information lower bounds.',17,'normal','middle',MID)]
    finish(p,'figure2_reachability.svg')


def figure3():
    p=base('Supporting result: a sharp fluctuation envelope with two sources of slack')
    p += [rect(140,85,1320,100,LIGHT),t(800,128,'σ_eff² ≤ (λ g_max)² / 4 × (1 + r_max) / (1 − r_max)',26,'bold','middle'),t(800,162,'extremal structural range × maximal temporal amplification',20,'normal','middle',MID)]
    p += [t(45,250,'A',28,'bold'),t(85,250,'Persistence amplifies temporal variance',25,'bold'),t(735,250,'B',28,'bold'),t(775,250,'Exact slack decomposition',25,'bold')]
    x0,y0,x1,y1=90,590,665,300
    p += [line(x0,y0,x0,y1),line(x0,y0,x1,y0),t(380,635,'community eigenvalue r',18,'normal','middle'),t(30,455,'f(r)',18,'normal')]
    for rv in [0,.3,.6,.9]:
        x=x0+rv/.9*(x1-x0); p += [line(x,y0,x,y0+7),t(x,y0+30,f'{rv:.1f}',15,'normal','middle')]
    for vv in [1,5,10,15,20]:
        y=y0-(vv-1)/(20-1)*(y0-y1); p += [line(x0-7,y,x0,y),t(x0-15,y+5,str(vv),15,'normal','end')]
    pts=[]
    for i in range(200):
        r=.9*i/199; f=(1+r)/(1-r); x=x0+r/.9*(x1-x0); y=y0-(f-1)/(20-1)*(y0-y1); pts.append((x,y))
    p += [poly(pts,BLACK,3),t(380,335,'f(r) = (1+r)/(1−r)',18,'bold','middle')]
    p += [rect(785,320,330,135,WHITE),t(950,355,'1. Range / variance',22,'bold','middle'),t(950,393,'4 Varπ(s) / (λ g_max)²',20,'normal','middle',MID),t(950,430,'≤ 1',20,'normal','middle',MID),t(1160,400,'×',42,'bold','middle'),rect(1205,320,330,135,WHITE),t(1370,355,'2. Slow-mode alignment',22,'bold','middle'),t(1370,393,'Σ w̃_j f(r_j) / f(r_max)',19,'normal','middle',MID),t(1370,430,'≤ 1',20,'normal','middle',MID),line(1160,470,1160,525,arrow=True),rect(950,535,420,95,LIGHT),t(1160,570,'realized / extremal',22,'bold','middle'),t(1160,607,'σ_eff² / B = factor 1 × factor 2',19,'normal','middle',MID)]
    p += [t(45,690,'C',28,'bold'),t(85,690,'Equality witness versus a three-state loose example',25,'bold'),rect(100,725,640,120,WHITE),t(420,760,'Extremal equality witness',21,'bold','middle'),t(420,790,'two-state symmetric chain + endpoint rewards',18,'normal','middle',MID),t(420,818,'range saturation = 1; slow-mode alignment = 1',18,'normal','middle',MID),t(420,840,'σ_eff² / B = 1',18,'normal','middle',MID),rect(870,725,630,120,WHITE),t(1185,760,'Three-state reversible fixture',21,'bold','middle'),t(1185,790,'eigenvalues 1, 0.7, 0.1; rewards (0,1,0)',18,'normal','middle',MID),t(1185,818,'range saturation = 8/9; slow-mode alignment = 11/51',18,'normal','middle',MID),t(1185,840,'σ_eff² / B = 88/459 ≈ 0.192',18,'normal','middle',MID),t(800,882,'Sharp means equality is attainable; it does not mean a generic multi-state system lies near the ceiling.',20,'bold','middle')]
    finish(p,'figure3_extremal_envelope.svg')


def figure4():
    p=base('Long-term similarity can hide different return dynamics','Only a model-compatible complex local mode has the stronger diagnostic implication G > 0.')
    left=[45,440,835,1230]; titles=['Directional accumulation','Neutral cancellation','Monotone restoration','Oscillatory restoration']; labs=['A','B','C','D']
    for x,lbl,title in zip(left,labs,titles): p += [t(x,150,lbl,28,'bold'),t(x+42,150,title,23,'bold')]
    for x in left: p += [rect(x,180,330,325,WHITE,GRID,0,2),line(x,340,x+330,340,stroke=GRID,sw=2,dash='7 6'),t(x+165,540,'time',16,'normal','middle',MID)]
    def mapxy(xbase, tt, yy): return (xbase+tt/24*330, 340-yy/1.0*140)
    tt=list(range(25))
    p.append(poly([mapxy(left[0],i,.12+.035*i) for i in tt],BLACK,3))
    tri=[0,.36,0,-.02]*7; p.append(poly([mapxy(left[1],i,tri[i]) for i in tt],BLACK,3))
    p.append(poly([mapxy(left[2],i,.85*(.73**i)) for i in tt],BLACK,3))
    osc=[0]*25; osc[0]=.85; osc[1]=.55
    for i in range(23): osc[i+2]=1.5*osc[i+1]-.75*osc[i]
    p.append(poly([mapxy(left[3],i,osc[i]) for i in tt],BLACK,3))
    notes=[('persistent mean bias','net displacement accumulates','trend'),('period drift = 0','period map multiplier = 1','mechanistic proposition'),('real stable modes','G = 0 can remain compatible','attractive return'),('α = 1, φ = 0.5, G = 0.5','complex stable mode; period = 12','diagnostic theorem')]
    for x,(a,b,c) in zip(left,notes):
        p += [t(x+165,585,a,18,'bold','middle'),t(x+165,613,b,17,'normal','middle'),rect(x+30,635,270,52,LIGHT),t(x+165,669,c,18,'bold','middle')]
    p += [rect(85,720,1430,115,LIGHT),t(300,758,'Stable real modes',20,'bold','middle'),t(300,795,'may admit φ = r₁, α = r₂ ⇒ G = 0',17,'normal','middle'),t(800,758,'Model-compatible complex mode',20,'bold','middle'),t(800,795,'0 ≤ T < 2 and discriminant < 0 ⇒ every feasible decomposition has G > 0',17,'normal','middle'),t(1320,758,'Outside trace domain',20,'bold','middle'),t(1320,795,'T < 0 or T ≥ 2 ⇒ model incompatible',17,'normal','middle'),t(800,875,'Cancellation and restoration can both look like stasis over long windows, but only restoration erases perturbations.',20,'bold','middle')]
    finish(p,'figure4_long_time_outcomes.svg')


def audit():
    assert h_star(2,2)==3
    assert [2+h_star(2,b) for b in range(2,7)]==[5,4,4,4,4]
    assert [2+h_star(2,2)+1 for _ in range(2,7)]==[6,6,6,6,6]
    assert pareto_fixture(3,4)==[(8,5,5,2),(7,6,6,3)]
    range_sat=8/9; align=11/51
    assert abs(range_sat*align-88/459)<1e-15
    alpha=1.; phi=.5; G=.5
    T=alpha+phi; D=alpha*phi+(1-phi)*G
    disc=T*T-4*D
    period=2*math.pi/math.acos(T/(2*math.sqrt(D)))
    assert abs(disc+0.75)<1e-15 and abs(period-12)<1e-12 and 0<=T<2

if __name__=='__main__':
    audit(); figure1(); figure2(); figure3(); figure4()
