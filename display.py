import pygame

class Screen():
    def __init__(self,screen):
        self.screen=screen
        il=lambda x:pygame.image.load(f'src\\img\\{x}.bmp')
        self.bg=il('bg')
        self.figure=pygame.transform.scale_by(il('figure'),0.3)
        self.hi=il('hi')
        self.score=il('score')
        self.sound=il('sound')
        self.sl=il('sl')
        self.pause=il('pause')
        self.gameover=il('gameover')
        self.bg_color=(137,151,117)
        self.font=pygame.font.Font('src\\fonts\\Segment7Standard.otf',12)
        
    def _dot(self,x,y):
        pygame.draw.rect(self.screen,0,(x,y,9,9))
        pygame.draw.rect(self.screen,self.bg_color,(x+1,y+1,7,7))
        pygame.draw.rect(self.screen,0,(x+2,y+2,5,5))
    def draw(self,disp_ram,shared_ram):
        canvas,subcanvas=disp_ram['canvas'],disp_ram['subcanvas']
        self.screen.blit(self.bg,(0,0))
        for i in range(20):
            for j in range(10):
                if canvas[i][j]:
                    self._dot(5+j*10,5+i*10)

        score_text='%04d'%shared_ram['score']
        self.screen.blit(self.font.render(score_text,False,0),(113,5))
        self.screen.blit(self.font.render('00',False,0),(143,5))

        #self.screen.blit(self.hi,(113,20))
        self.screen.blit(self.score,(123,20))
        if shared_ram['sound']:
            self.screen.blit(self.sound,(150,20))

        for i in range(4):
            if subcanvas[i]:
                self._dot(113+i*10,40)
        for i in range(4):
            if subcanvas[i+4]:
                self._dot(123+(i%2)*10,50+(i//2)*10)
        
        sl_text='%2d %2d'%(shared_ram['speed'],shared_ram['level'])
        self.screen.blit(self.font.render(sl_text,False,0),(113,95))
        self.screen.blit(self.sl,(110,110))
        
        self.screen.blit(self.figure,(110,130))
        #self.screen.blit(self.pause,(110,170))
        #self.screen.blit(self.gameover,(110,180))
        
        pygame.display.flip()
