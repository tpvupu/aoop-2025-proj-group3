import pygame
from UI.components.base_scene import BaseScene, draw_wrapped_text
from UI.components.character_animator import CharacterAnimator
from UI.components.audio_manager import AudioManager
import setting


class AdviceScene(BaseScene):
    """心理測驗結果與學習建議專題場景"""

    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.audio = AudioManager.get_instance()
        
        # 背景
        self.background = pygame.image.load(
            setting.ImagePath.BACKGROUND_PATH
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )
        self.background.set_alpha(80)
        
        # 字體
        self.title_font = pygame.font.Font(setting.JFONT_PATH_BOLD, 52)
        self.section_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 32)
        self.content_font = pygame.font.Font(setting.JFONT_PATH_Light, 26)
        
        # 角色動畫
        self.animator = CharacterAnimator(
            self.player.ending, (100, 350), (250, 250)
        )
        self.animator.frame_delay = 3
        
        # 建議文本
        self.advice_text = None
        self.is_loading = True
        
        # 返回按鈕提示
        self.prompt_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 24)
        self.prompt_text = "(按 ESC 或 Enter 返回)"
        self.prompt_surface = self.prompt_font.render(
            self.prompt_text, True, (100, 100, 100)
        )
        
        # 顯示位置
        self.content_rect = pygame.Rect(400, 80, 750, 700)
        
        # 生成建議
        self._generate_advice()
    
    def _generate_advice(self):
        """背景生成建議"""
        try:
            from services.feedback_generator import generate_final_advice
            self.advice_text = generate_final_advice(self.player)
            self.audio.play_sound(setting.SoundEffect.BLING_PATH)
        except Exception as e:
            self.advice_text = f"(產生建議失敗)\n\n{str(e)}"
            self.audio.play_sound(setting.SoundEffect.DONG_PATH)
        finally:
            self.is_loading = False
    
    def update(self):
        """更新動畫與狀態"""
        self.animator.update()
    
    def draw(self):
        """繪製場景"""
        self.screen.fill((245, 240, 225))
        self.screen.blit(self.background, (0, 0))
        
        # 半透明黑色遮罩
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 30))
        self.screen.blit(overlay, (0, 0))
        
        # 標題
        title = self.title_font.render("個人建議", True, (50, 50, 70))
        title_rect = title.get_rect(topleft=(400, 15))
        self.screen.blit(title, title_rect)
        
        # 角色動畫
        self.animator.draw(self.screen)
        
        # 建議內容面板
        panel_bg = pygame.Surface(
            (self.content_rect.width + 20, self.content_rect.height + 20),
            pygame.SRCALPHA
        )
        panel_bg.fill((255, 255, 255, 200))
        self.screen.blit(
            panel_bg,
            (self.content_rect.left - 10, self.content_rect.top - 10)
        )
        
        # 面板邊框
        border_rect = pygame.Rect(
            self.content_rect.left - 10,
            self.content_rect.top - 10,
            self.content_rect.width + 20,
            self.content_rect.height + 20
        )
        pygame.draw.rect(self.screen, (120, 120, 160), border_rect, 3)
        
        # 建議文本
        if self.is_loading:
            loading_text = self.content_font.render("正在生成建議...", True, (100, 100, 100))
            self.screen.blit(
                loading_text,
                (self.content_rect.centerx - loading_text.get_width() // 2, self.content_rect.centery - 20)
            )
        elif self.advice_text:
            draw_wrapped_text(
                self.screen,
                self.advice_text,
                self.content_font,
                self.content_rect,
                (30, 30, 30),
                32
            )
        
        # 返回提示
        prompt_rect = self.prompt_surface.get_rect(
            bottomright=(self.SCREEN_WIDTH - 20, self.SCREEN_HEIGHT - 20)
        )
        self.screen.blit(self.prompt_surface, prompt_rect)
        
        pygame.display.flip()
    
    def run(self):
        """主循環"""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        self.audio.play_sound(setting.SoundEffect.DONG_PATH)
                        return "END"
            
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
