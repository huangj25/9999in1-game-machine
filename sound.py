import pygame
pygame.mixer.init()
sound_idx=['pagedown','drive','boom','hit','putshoot','move',
           'open','start','gameover','levelup']
sounds={}
pygame.mixer.set_num_channels(1)
channel = pygame.mixer.Channel(0)
for i in sound_idx:
    sounds[i]=pygame.mixer.Sound(f'src\\sound\\{i}.wav')
available=True
def getidle():
    global available
    busy=pygame.mixer.get_busy()
    if busy and not available:
        return False
    else:
        available=True
        return True
        
def play(sound,no_interrupt=False):
    global available
    if getidle():
        channel.play(sounds[sound])
        if no_interrupt:
            available=False

def playloop(sound):
    sounds[sound].play(loops=-1)

def stop(sound):
    sounds[sound].stop()

def clear():
    pygame.mixer.stop()
