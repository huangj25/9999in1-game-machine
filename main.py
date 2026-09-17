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
#游戏函数定义
def openSceneTick():
    pass
def selectSceneTick():
    pass
def gameTankWarTick():
    pass
def gameShootingTick():
    pass
gameTickFun=[gameTankWarTick,gameShootingTick]
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
    time.sleep(0.01)
