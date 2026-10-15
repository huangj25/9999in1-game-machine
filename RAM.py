shared_ram={
    'open':True,
    'selected':0,
    'version':1,
    'state':0, #0=开屏动画，1=选择界面，2=游戏中
    'speed':1,
    'level':1,
    'pause':False,
    'sound':True,
    'score':0,
    'hi-score':0,
}
uram={}
inp=['',False,False,False]#key, hold, shift, hold
disp_ram={
    'canvas':[[0 for _ in range(10)] for _ in range(20)],
    'subcanvas':[0 for _ in range(8)],#显示剩余生命、即将出现的方块等
    'vertical_flip':False
}

