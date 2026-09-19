from display import Screen
from ROM import *
import pygame,time
screen=pygame.display.set_mode((160,208))
scr=Screen(screen)
key_dict={
    pygame.K_w:'U',
    pygame.K_a:'L',
    pygame.K_s:'D',
    pygame.K_d:'R',
    pygame.K_UP:'U',
    pygame.K_LEFT:'L',
    pygame.K_DOWN:'D',
    pygame.K_RIGHT:'R',
    pygame.K_RSHIFT:'shift',
    pygame.K_SPACE:'shift',
    pygame.K_1:'s/p',
    pygame.K_2:'on/off'
}
pressed={
    'L':False,
    'R':False,
    'U':False,
    'D':False,
    'shift':False,
    's/p':False,
    'on/off':False,
    'reset':False,
    'sound':False
}
#模拟RAM
shared_ram={
    'open':True,
    'selected':0,
    'version':1,
    'state':0, #0=开屏动画，1=选择界面，2=游戏中
    'pause':False,
    'sound':True,
    'score':0,
    'hi-score':0,
}
unique_ram={}
inp={#记录按键按下的帧数
    'L':0,
    'R':0,
    'U':0,
    'D':0,
    'shift':0,
    's/p':0,
    'on/off':0,
    'reset':0,
    'sound':0
}
disp_ram={
    'canvas':[[0 for _ in range(10)] for _ in range(20)],
    'subcanvas':[0 for _ in range(8)],#显示剩余生命、即将出现的方块等
    'level':0,
    'speed':0
}

def hold(key,delay=100,loop=30):
    return inp[key]==1 or (inp[key]>delay and (inp[key]-delay)%loop==0)
#游戏函数定义
def openSceneTick():
    if not unique_ram:
        unique_ram.update({'step':1,'sleep':0,'blink':0,'r':19,'c':0})
        for r in range(20):
            disp_ram['canvas'][r][:]=map(int,open_logo[r])
    if inp['U'] or inp['D'] or inp['L'] or inp['R'] or inp['shift']:
        unique_ram.clear()
        shared_ram['state']=1
        return
    if inp['s/p']:
        shared_ram['state']=2
        unique_ram.clear()
        return
    if unique_ram['sleep']:
        unique_ram['sleep']-=1
    elif unique_ram['step']==1:
        r=unique_ram['r'];c=unique_ram['c']
        disp_ram['canvas'][r][c]^=1
        d=int(spiral_map[r][c])
        if d==0:
            unique_ram['step']=2;unique_ram['blink']=0;unique_ram['timer']=0
            return
        elif d==1:c+=1
        elif d==2:r-=1
        elif d==3:c-=1
        else:r+=1
        unique_ram['r']=r;unique_ram['c']=c
        unique_ram['sleep']=3
    else:
        for i in range(20):
            for c in range(10):
                disp_ram['canvas'][i][c]^=int(open_logo[i][c])
        unique_ram['blink']+=1
        if unique_ram['blink']>=10:
            unique_ram['step']=1
            unique_ram['r']=19;unique_ram['c']=0
        unique_ram['sleep']=150
def selectSceneTick():
    if not unique_ram:
        unique_ram.update({'absleep':0,'abstep':0,'demosleep':0,'demostep':0,'map':shared_ram['selected']})
        disp_ram['canvas']=[[0 for _ in range(10)] for _ in range(20)]
    if hold('shift'):
        shared_ram['selected']+=1
        if shared_ram['selected']==26:
            shared_ram['selected']=0
        unique_ram['map']=shared_ram['selected'] if shared_ram['selected']<=10 else 10
        if shared_ram['version']>versions[unique_ram['map']]:
            shared_ram['version']=1
        unique_ram.update({'absleep':0,'abstep':0,'demosleep':0,'demostep':0})
    if inp['s/p']:
        shared_ram['state']=2
        unique_ram.clear()
        return
    if unique_ram['absleep']:
        unique_ram['absleep']-=1
    else:
        f=[0,1,2,3,4,3,2,1,0][unique_ram['abstep']]
        for i in range(5):
            for j in range(5):
                disp_ram['canvas'][i+9][j+2]=int(alphabet_map[shared_ram['selected']][f][i][j])
        unique_ram['abstep']+=1
        if unique_ram['abstep']==9:
            unique_ram['abstep']=0
            unique_ram['absleep']=120
        else:
            unique_ram['absleep']=60
    if unique_ram['demosleep']:
        unique_ram['demosleep']-=1
    else:
        for i in range(8):
            for j in range(10):
                disp_ram['canvas'][i][j]=int(demo_map[unique_ram['map']][unique_ram['demostep']].split()[i][j])
        unique_ram['demostep']+=1
        if unique_ram['demostep']==4:
            unique_ram['demostep']=0
        unique_ram['demosleep']=300
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
    pass
def gameFillingTick():
    pass
def gameSnakeTick():
    pass
def gameFrogTick():
    pass
def gameTetrisTick():
    pass
gameTickFun=[gameTankWarTick,gameShootingTick]
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            raise SystemExit()
        elif event.type==pygame.KEYDOWN:
            if key_dict.get(event.key):
                pressed[key_dict[event.key]]=True
        elif event.type==pygame.KEYUP:
            if key_dict.get(event.key):
                pressed[key_dict[event.key]]=False
    for key in pressed:
        if pressed[key]:
            inp[key]+=1
        elif inp[key]:
            inp[key]=0
    if shared_ram['state']==0:
        openSceneTick()
    elif shared_ram['state']==1:
        selectSceneTick()
    else:
        gameTickFun[shared_ram['selected']]()
    scr.draw(disp_ram,shared_ram)
    time.sleep(0.002)
