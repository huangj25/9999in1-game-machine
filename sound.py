import pygame
pygame.mixer.init()
sound_idx=['pagedown','drive','boom','hit','putshoot','move',
           'open','start','gameover','levelup']
sounds={}
pygame.mixer.set_num_channels(1)
channel = pygame.mixer.Channel(0)
for i in sound_idx:
    sounds[i]=pygame.mixer.Sound(f'src\\sound\\{i}.wav')

def play(sound):
    channel.play(sounds[sound])

def playloop(sound):
    sounds[sound].play(loops=-1)

def stop(sound):
    sounds[sound].stop()

def clear():
    pygame.mixer.stop()
