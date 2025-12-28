import pygame
import setting

class FirstScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        
    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.FINGERDOWN):
                    # 使用者互動，結束 FirstScene
                    return "START"
            # 載入一張圖片
            background_image = pygame.image.load(setting.ImagePath.FIRST_SCENE_PATH).convert()
            background_image = pygame.transform.smoothscale(background_image, (self.screen.get_width(), self.screen.get_height()))
            # 確保圖片大小符合螢幕
            #background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
            # 在螢幕上繪製圖片
            self.screen.blit(background_image, (0, 0))
            
            
            
            pygame.display.flip()
            
            clock.tick(60)