from ROM import *
from RAM import *
import sound
import random

def hold(key,delay=100,loop=50):
    return inp[key]==1 or (inp[key]>delay and (inp[key]-delay)%loop==0)
def gameWithLifeAnimTick():
    if uram['anim']=='boom':
        if uram['anim_t']%20==0:
            bi,bj=uram['boom_pos']
            fnum=[0,1,2,3,2,3,2,1]*4
            for i in range(5):
                for j in range(5):
                    disp_ram['canvas'][bi+i][bj+j]=int(boom[fnum[uram['aframe']]].split()[i][j])
            uram['aframe']+=1
            if uram['aframe']==32:
                uram['aframe']=0
                if uram['life']==0:
                    uram['anim']='slowcl'
                else:
                    uram['anim']='fastcl'
        
        uram['anim_t']+=1
    elif uram['anim']=='fastcl':
        uram['anim']=None
        return 1
    


def openSceneTick():
    global uram
    if not uram:
        sound.play('open')
        uram.update({'step':1,'sleep':0,'blink':0,'r':19,'c':0})
        for r in range(20):
            disp_ram['canvas'][r][:]=map(int,open_logo[r])
    if inp['U'] or inp['D'] or inp['L'] or inp['R'] or inp['shift']:
        sound.play('pagedown')
        uram.clear()
        shared_ram['state']=1
        return
    if inp['s/p']:
        sound.play('start')
        shared_ram['state']=2
        uram.clear()
        return
    if uram['sleep']:
        uram['sleep']-=1
    elif uram['step']==1:
        r=uram['r'];c=uram['c']
        disp_ram['canvas'][r][c]^=1
        d=int(spiral_map[r][c])
        if d==0:
            uram['step']=2;uram['blink']=0;uram['timer']=0
            return
        elif d==1:c+=1
        elif d==2:r-=1
        elif d==3:c-=1
        else:r+=1
        uram['r']=r;uram['c']=c
        uram['sleep']=3
    else:
        for i in range(20):
            for c in range(10):
                disp_ram['canvas'][i][c]^=int(open_logo[i][c])
        uram['blink']+=1
        if uram['blink']>=10:
            uram['step']=1
            uram['r']=19;uram['c']=0
        uram['sleep']=150
def selectSceneTick():
    if not uram:
        uram.update({
            'absleep':0,
            'abstep':0,
            'demosleep':0,
            'demostep':0,
            'map':shared_ram['selected']
        })
        disp_ram['canvas']=[[0 for _ in range(10)] for _ in range(20)]
    if hold('shift'):
        sound.play('pagedown')
        shared_ram['selected']+=1
        if shared_ram['selected']==26:
            shared_ram['selected']=0
        uram['map']=shared_ram['selected'] if shared_ram['selected']<=10 else 10
        if shared_ram['version']>versions[uram['map']]:
            shared_ram['version']=1
        uram.update({'absleep':0,'abstep':0,'demosleep':0,'demostep':0})
    if hold('L'):
        sound.play('pagedown')
        shared_ram['level']+=1
        if shared_ram['level']>10:
            shared_ram['level']=1
    if hold('R'):
        sound.play('pagedown')
        shared_ram['speed']+=1
        if shared_ram['speed']>10:
            shared_ram['speed']=1
    if inp['s/p']:
        sound.play('start')
        shared_ram['state']=2
        uram.clear()
        return
    if uram['absleep']:
        uram['absleep']-=1
    else:
        f=[0,1,2,3,4,3,2,1,0][uram['abstep']]
        for i in range(5):
            for j in range(5):
                disp_ram['canvas'][i+9][j+2]=int(alphabet_map[shared_ram['selected']][f][i][j])
        uram['abstep']+=1
        if uram['abstep']==9:
            uram['abstep']=0
            uram['absleep']=120
        else:
            uram['absleep']=60
    if uram['demosleep']:
        uram['demosleep']-=1
    else:
        for i in range(8):
            for j in range(10):
                disp_ram['canvas'][i][j]=int(demo_map[uram['map']][uram['demostep']].split()[i][j])
        uram['demostep']+=1
        if uram['demostep']==4:
            uram['demostep']=0
        uram['demosleep']=300
def gameTankWarTick():
    pass
def gamePingPongTick():
    pass
def gameAlienTick():
    pass
def gameMarbleTick():
    pass
def gameCarTick():
    pass
def gameCarRoadTick():
    pass
def gameShootingTick():
    global uram
    if not uram:
        uram.update({'pos':4,'life':4,'t':0,'bullet':-2,'bcol':-1,'anim':None,'anim_t':0,'boom_pos':(0,0),
                     'aframe':0})
        disp_ram['canvas'] = [[0]*10 for _ in range(20)]
        return
    if uram['anim']:
        if gameWithLifeAnimTick():
            if not uram['life']:
                uram.clear()
                shared_ram['state']=1
            else:
                sound.play('start')
        return

    if hold('L'):
        sound.play('move')
        uram['pos'] = max(0,uram['pos']-1)
    if hold('R'):
        sound.play('move')
        uram['pos'] = min(9,uram['pos']+1)

    if hold('shift') and uram['bullet']<0:
        sound.play('hit')
        uram['bullet']=17
        uram['bcol']=uram['pos']
    pos=uram['pos']
    if uram['bullet']>=-1:
        y,x=uram['bullet'],uram['bcol']
        if disp_ram['canvas'][y][x]==1 or y==-1:
            for yy in range(17,y-1,-1):
                disp_ram['canvas'][yy][x]=0
            if uram['bullet']!=-1:
                shared_ram['score']+=1
            uram['bullet']=-2
        else:
            disp_ram['canvas'][y][x]=1
            uram['bullet']-=1
    elif uram['t']>=100:
        for y in range(18,0,-1):
            disp_ram['canvas'][y]=disp_ram['canvas'][y-1]
        disp_ram['canvas'][0] = [1 if random.random() < 0.3 else 0 for _ in range(10)]
        if any(disp_ram['canvas'][18][x] == 1 for x in range(10)):
            uram['life']-=1
            uram['anim']='boom'
            uram['boom_pos']=(15,max(0,min(5,pos-1)))
            uram['anim_t']=0
            uram['bullet']=-1
            sound.play('boom')
        uram['t']=0
    disp_ram['canvas'][18:]=[[0]*10 for _ in range(2)]
    disp_ram['canvas'][18][pos]=1
    disp_ram['canvas'][19][pos]=1
    if pos>0:
        disp_ram['canvas'][19][pos-1]=1
    if pos<9:
        disp_ram['canvas'][19][pos+1]=1

    uram['t']+=1
    
    
def gameFillingTick():
    pass
def gameSnakeTick():
    pass
def gameFrogTick():
    pass
def gameTetrisTick():
    pass
