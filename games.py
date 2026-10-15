from ROM import *
from RAM import *
import sound
import random

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
                for i in range(5):
                    for j in range(5):
                        disp_ram['canvas'][bi+i][bj+j]=0
                uram['aframe']=0
                uram['anim_t']=0
                if uram['life']==0:
                    uram['anim']='slowcl'
                    sound.play('gameover')
                else:
                    uram['anim']='fastcl'
                return
        
        uram['anim_t']+=1
    elif uram['anim']:
        if uram['anim_t']%(5 if uram['anim']=='fastcl' else 35)==0:
            if uram['aframe']<=19:
                disp_ram['canvas'][19-uram['aframe']]=[1]*10
            else:
                disp_ram['canvas'][uram['aframe']-20]=[0]*10
            uram['aframe']+=1
        if uram['aframe']==40:
            uram['anim']=None
            uram['anim_t']=0
            uram['aframe']=0
            return 1
        uram['anim_t']+=1
def draw_ship():
    pos=uram['pos']
    disp_ram['canvas'][18:]=[[0]*10 for _ in range(2)]
    disp_ram['canvas'][18][pos]=1
    disp_ram['canvas'][19][pos]=1
    if pos>0:
        disp_ram['canvas'][19][pos-1]=1
    if pos<9:
        disp_ram['canvas'][19][pos+1]=1
def draw_digit(n,bi,bj):
    a=n//10
    b=n%10
    for i in range(5):
        for j in range(3):
            disp_ram['canvas'][bi+i][bj+j]=int(digit_map[a].split()[i][j])
            disp_ram['canvas'][bi+i][bj+j+4]=int(digit_map[b].split()[i][j])

def openSceneTick():
    global uram
    if not uram:
        sound.play('open')
        uram.update({'step':1,'sleep':0,'blink':0,'r':19,'c':0})
        for r in range(20):
            disp_ram['canvas'][r][:]=map(int,open_logo[r])
    if inp[0] in ['U','D','L','R','Us','Ds','Ls','Rs'] or inp[2]:
        sound.play('pagedown')
        uram.clear()
        shared_ram['state']=1
        return
    if inp[0]=='s/p':
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
            'map':shared_ram['selected'],
            'shiftsleep':100,
            'keysleep':100
        })
        disp_ram['canvas']=[[0 for _ in range(10)] for _ in range(20)]
        draw_digit(shared_ram['version'],15,1)
    if inp[2] and not uram['shiftsleep']:
        sound.play('pagedown')
        shared_ram['selected']+=1
        if shared_ram['selected']==26:
            shared_ram['selected']=0
        uram['map']=shared_ram['selected'] if shared_ram['selected']<=10 else 10
        if shared_ram['version']>versions[uram['map']]:
            shared_ram['version']=1
        uram.update({'absleep':0,'abstep':0,'demosleep':0,'demostep':0})
        uram['shiftsleep']=50 if inp[3] else 100
    elif not inp[2]:
        uram['shiftsleep']=0
            
    if inp[0]=='L' and not uram['keysleep']:
        sound.play('pagedown')
        shared_ram['level']+=1
        if shared_ram['level']>10:
            shared_ram['level']=1
        uram['keysleep']=70 if inp[1] else 300
    elif inp[0]=='R' and not uram['keysleep']:
        sound.play('pagedown')
        shared_ram['speed']+=1
        if shared_ram['speed']>10:
            shared_ram['speed']=1
        uram['keysleep']=70 if inp[1] else 300
    elif inp[0]=='U' and not uram['keysleep']:
        sound.play('pagedown')
        shared_ram['version']+=1
        if shared_ram['version']>versions[uram['map']]:
            shared_ram['version']=1
        uram['keysleep']=70 if inp[1] else 300
        draw_digit(shared_ram['version'],15,1)
    elif inp[0]=='D' and not uram['keysleep']:
        sound.play('pagedown')
        shared_ram['version']-=1
        if shared_ram['version']==0:
            shared_ram['version']=versions[uram['map']]
        uram['keysleep']=70 if inp[1] else 300
        draw_digit(shared_ram['version'],15,1)
    elif inp[0]=='s/p':
        shared_ram['state']=2
        uram.clear()
        return
    elif not inp[0]:
        uram['keysleep']=0

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
    if uram['keysleep']:
        uram['keysleep']-=1
    if uram['shiftsleep']:
        uram['shiftsleep']-=1
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
    #初始化
    if not uram:
        uram.update({'pos':4,'life':4,'t':0,'b1':-2,'b1col':-1,
                     'b2':-2,'b2col':-1,'anim':None,'anim_t':0,'boom_pos':(0,0),
                     'aframe':0,'keysleep':0,'shiftsleep':0})
        disp_ram['canvas'] = [[0]*10 for _ in range(20)]
        for i in range(shared_ram['level']-1):
            disp_ram['canvas'][i]=[random.randint(0,1) for _ in range(10)]
        disp_ram['subcanvas']=[1]*4+[0]*4
        disp_ram['vertical_flip']=(shared_ram['version']-1)//2
        draw_ship()
        sound.play('start',True)
        return
    #播放动画
    if uram['anim']:
        if gameWithLifeAnimTick():
            if not uram['life']:
                if shared_ram['score']>shared_ram['hi-score']:
                    shared_ram['hi-score']=shared_ram['score']
                uram.clear()
                disp_ram['vertical_flip']=False
                shared_ram['state']=1
            else:
                uram['pos']=4
                for i in range(shared_ram['level']-1):
                    disp_ram['canvas'][i]=[random.randint(0,1) for _ in range(10)]
                draw_ship()
                sound.play('start',True)
        return
    if not sound.getidle():
        return
    
    #处理事件
    for b in ['b1','b2']:
        if uram[b]>=-1:
            y,x=uram[b],uram[b+'col']
            if disp_ram['canvas'][y][x]==1 or y==-1:
                for yy in range(17,max(y-1,-1),-1):
                    disp_ram['canvas'][yy][x]=0
                if uram[b]!=-1:
                    shared_ram['score']+=1
                uram[b]=-2
            else:
                disp_ram['canvas'][y][x]=1
                uram[b]-=1
            
    if uram['t']>=400-28*(shared_ram['speed']-1) and (uram['b1'],uram['b2'])==(-2,-2):
        if any(disp_ram['canvas'][17][x] == 1 for x in range(10)):
            uram['life']-=1
            disp_ram['subcanvas'][uram['life']]=0
            uram['anim']='boom'
            uram['boom_pos']=(15,max(0,min(5,uram['pos']-1)))
            uram['anim_t']=0
            uram['b1']=uram['b2']=-2
            sound.play('boom')
        for x in range(10):
            disp_ram['canvas'][18][x]|=disp_ram['canvas'][17][x]
        for y in range(17,0,-1):
            disp_ram['canvas'][y]=disp_ram['canvas'][y-1]
        disp_ram['canvas'][0] = [random.randint(0,1) for _ in range(10)]
        uram['t']=0
    else:
        #响应按键
        if inp[0]=='L' and not uram['keysleep']:
            if uram['pos']>0:
                uram['pos']=uram['pos']-1
                sound.play('move')
                draw_ship()
            uram['keysleep']=20 if inp[1] else 100
        elif inp[0]=='R' and not uram['keysleep']:
            if uram['pos']<9:
                uram['pos']=uram['pos']+1
                sound.play('move')
                draw_ship()
            uram['keysleep']=20 if inp[1] else 100
        elif not inp[0]:
            uram['keysleep']=0
        if inp[2] and not uram['shiftsleep']:
            sound.play('hit')
            if (shared_ram['version']-1)%2:
                if uram['pos']>0:
                    uram['b1']=17
                    uram['b1col']=uram['pos']-1
                if uram['pos']<9:
                    uram['b2']=17
                    uram['b2col']=uram['pos']+1
            else:
                uram['b1']=17
                uram['b1col']=uram['pos']
            uram['shiftsleep']=50 if inp[3] else 70
        elif not inp[2]:
            uram['shiftsleep']=0

    uram['t']+=1
    if uram['keysleep']:
        uram['keysleep']-=1
    if uram['shiftsleep']:
        uram['shiftsleep']-=1

def gameFillingTick():
    pass
def gameSnakeTick():
    pass
def gameFrogTick():
    pass
def gameTetrisTick():
    pass
