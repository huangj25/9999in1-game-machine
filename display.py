import pygame

class Screen():
    def __init__(self,screen):
        self.screen=screen
        self.bg=pygame.image.load('src\\img\\bg.bmp')
        self.bg_color=(137,151,117)
    def draw(self,disp_ram,shared_ram):
        canvas=disp_ram['canvas']
        self.screen.blit(self.bg,(0,0))
        for i in range(20):
            for j in range(10):
                if canvas[i][j]:
                    pygame.draw.rect(self.screen,0,(5+j*10,5+i*10,9,9))
                    pygame.draw.rect(self.screen,self.bg_color,(6+j*10,6+i*10,7,7))
                    pygame.draw.rect(self.screen,0,(7+j*10,7+i*10,5,5))
        #先忽略没画完的其他东西……
        pygame.display.flip()
