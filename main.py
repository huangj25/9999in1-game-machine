from display import Screen
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

#模拟ROM
open_logo=[#开机画面
     '0000000000','0111000000','0101000000','0111000000','0001000000',
     '0111011100','0000010100','0000011100','0000000100','0000011100',
     '0111000000','0101000000','0111000000','0001000000','0111011100',
     '0000010100','0000011100','0000000100','0000011100','0000000000']
spiral_map=[#螺旋方向图
    '4333333333','4433333332','4443333322','4444333222','4444432222',
    '4444422222','4444422222','4444422222','4444422222','4444422222',
    '4444422222','4444422222','4444422222','4444422222','4444022222',
    '4441122222','4411112222','4111111222','1111111122','1111111112']
number_map=[
    '111 101 101 101 111',
    '010 110 010 010 111',
    '111 001 111 100 111',
    '111 001 111 001 111',
    '101 101 111 001 001',
    '111 100 111 001 111',
    '111 100 111 101 111',
    '111 001 001 001 001',
    '111 101 111 101 111',
    '111 101 111 001 111'
]
#模拟RAM
shared_ram={
    'open':True,
    'selected':0,
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
    'canvas':[[1 for _ in range(10)] for _ in range(20)],
    'subcanvas':[0 for _ in range(8)],#显示剩余生命、即将出现的方块等
    'level':0,
    'speed':0
}
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
    pass
def gameTankWarTick():
    pass
def gameShootingTick():
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
