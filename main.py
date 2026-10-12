from display import Screen
from games import *
import pygame,time
pygame.font.init()
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
gameTickFun=[gameShootingTick]
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
