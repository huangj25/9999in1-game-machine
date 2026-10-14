from display import Screen
from games import *
import pygame,time
import ctypes
pygame.font.init()
screen=pygame.display.set_mode((160,208))
hwnd = pygame.display.get_wm_info()['window']
imm32 = ctypes.WinDLL('imm32')
imm32.ImmAssociateContext(hwnd, 0)
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
    #shift键单独处理
    if pressed['shift']:
        if inp[2]:
            inp[3]=True
        else:
            inp[2]=True
    else:
        inp[2]=inp[3]=False
    #处理其他按键
    keyflip=set()
    for key in pressed:
        if pressed[key] and key!='shift':
            keyflip|={key}
    key_now=''
    if len(keyflip)==1:
        key_now=keyflip.pop()
    if key_now and key_now==inp[0]:
        inp[1]=True
    else:
        inp[0]=key_now
        inp[1]=False

    if shared_ram['state']==0:
        openSceneTick()
    elif shared_ram['state']==1:
        selectSceneTick()
    else:
        gameTickFun[shared_ram['selected']]()
    scr.draw(disp_ram,shared_ram)
    time.sleep(0.002)
