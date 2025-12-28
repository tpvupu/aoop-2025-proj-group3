from UI.components.base_scene import BaseScene
import asyncio
import setting
from UI.components.character_animator import CharacterAnimator
import pygame
from UI.components.audio_manager import AudioManager

class FeedbackScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.audio = AudioManager.get_instance()
        self.background = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)

        # 背景黑色遮罩
        self.overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay_alpha = 0

        # QRcode圖片
        self.qrcode_image = pygame.image.load(setting.ImagePath.FEEDBACK_PATH).convert_alpha()
        self.qrcode_image = pygame.transform.scale(self.qrcode_image, (500, 500))
        self.qrcode_rect = self.qrcode_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # 動畫
        self.animator = CharacterAnimator(setting.GIF_PATHS['FOUR_CHAR_FRAMES'], (950, 500), (200, 200))
        self.animator.frame_delay = 20


        self.animator2 = CharacterAnimator(setting.GIF_PATHS['FOUR_CHAR2_FRAMES'], (50, 500), (200, 200))
        self.animator2.frame_delay = 20

        # 提示詞
        self.prompt_text = "(按下 Enter 鍵返回)"
        self.prompt_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)
        self.prompt_surface = self.prompt_font.render(self.prompt_text, True, (255, 255, 255))
        self.prompt_rect = self.prompt_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))

        self.title_font = pygame.font.Font(setting.CFONT_PATH,  72)
        self.title_text = "Give Us Your Feedback!"
        self.title_surface = self.title_font.render(self.title_text, True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(topleft = (100, 40))

    def update(self):
        self.animator.update()
        self.animator2.update()

        # 透明遮罩淡入
        if self.overlay_alpha < 140:
            self.overlay_alpha = min(255, self.overlay_alpha + 5)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))

    def draw(self, screen):
        # 1. 畫背景
        screen.blit(self.background, (0, 0))
        # 2. 畫半透明黑幕
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))  # 這行很重要
        screen.blit(self.overlay_surface, (0, 0))
        # 3. 畫其他內容
        screen.blit(self.qrcode_image, self.qrcode_rect)
        self.animator.draw(screen)
        self.animator2.draw(screen)
        screen.blit(self.prompt_surface, self.prompt_rect)
        screen.blit(self.title_surface, self.title_rect)

    async def run(self):
        self.running = True
        while self.running:
            await asyncio.sleep(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.audio.play_sound(setting.SoundEffect.DONG_PATH)
                        return

            self.update()
            self.draw(self.screen)
            pygame.display.flip()