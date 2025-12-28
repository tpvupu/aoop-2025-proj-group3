import pygame
import setting
import asyncio

class FirstScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self._bg = None
        
    async def run(self):
        self.running = True
        clock = pygame.time.Clock()
        # 預先載入背景圖片，失敗則使用純色背景
        if self._bg is None:
            try:
                img = pygame.image.load(setting.ImagePath.FIRST_SCENE_PATH).convert()
                self._bg = pygame.transform.smoothscale(img, (self.screen.get_width(), self.screen.get_height()))
            except Exception:
                # 載入失敗，使用純色背景以避免黑屏
                self._bg = None
        while self.running:
            await asyncio.sleep(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.FINGERDOWN):
                    # 使用者互動，結束 FirstScene
                    return "START"
            # 繪製背景
            if self._bg is not None:
                self.screen.blit(self._bg, (0, 0))
            else:
                # 純色背景 + 提示文字
                self.screen.fill((25, 25, 28))
                try:
                    font = pygame.font.SysFont(None, 42)
                    txt = font.render("Lazy Me Today Too", True, (240, 240, 240))
                    sub = font.render("點一下畫面開始", True, (200, 200, 200))
                    rect = txt.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 20))
                    rect2 = sub.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 20))
                    self.screen.blit(txt, rect)
                    self.screen.blit(sub, rect2)
                except Exception:
                    pass
            
            
            
            pygame.display.flip()
            
            clock.tick(60)