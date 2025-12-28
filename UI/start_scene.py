import pygame
from UI.components.base_scene import BaseScene
from UI.components.character_animator import CharacterAnimator
from UI.components.audio_manager import AudioManager
import setting
import asyncio

class StartScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.image.load(
            setting.ImagePath.BACKGROUND_PATH
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )
        self.background.set_alpha(100)

        self.title_font = pygame.font.Font(
            setting.MFONT_PATH, 72
        )
        self.subtitle_font = pygame.font.Font(
            setting.JFONT_PATH_REGULAR, 48
        )

        # ---------- 音樂 ----------    
        self.audio = AudioManager.get_instance()
        self.audio.play_bgm(setting.BGM.YIER_BUBU_PATH)


        # ---------- 按鈕 ----------
        self.buttons = []
        button_texts = [
            ("開始遊戲", "START"),
            ("遊戲介紹", "SHOW_INTRO"),
            ("調整音量", "SOUND_CONTROL"),
            ("退出遊戲", "QUIT"),
        ]
        button_w, button_h, spacing = 300, 70, 30
        total_h = len(button_texts) * (button_h + spacing) - spacing
        start_y = (self.SCREEN_HEIGHT - total_h) // 2 + 50

        for i, (text, action) in enumerate(button_texts):
            rect = pygame.Rect(
                (self.SCREEN_WIDTH - button_w) // 2,
                start_y + i * (button_h + spacing),
                button_w,
                button_h,
            )
            self.buttons.append(
                {
                    "rect": rect,
                    "text": text,
                    "action": action,
                    "hover": False,
                    "hovered_last": False,
                    "scale": 1.0,
                }
            )

        # ---------- 裝飾動畫 ----------
        self.animator1 = CharacterAnimator(setting.GIF_PATHS['FOUR_CHAR2_FRAMES'], (850, 400),(300, 300)) 
        self.animator2 = CharacterAnimator(setting.GIF_PATHS['FOUR_CHAR_FRAMES'] , (50, 400), (300, 300))
        self.animator1.frame_delay = 3
        self.animator2.frame_delay = 3
        # ---------- 其他 ----------
        self.selected_result = None

    # -------------------------------------------------------------
    # 更新邏輯 & 事件處理
    # -------------------------------------------------------------
    def update(self):
        self.clock.tick(self.FPS)
        self.animator1.update()
        self.animator2.update()
        mouse_pos = pygame.mouse.get_pos()

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["action"]

        # 按鈕 hover 更新
        for btn in self.buttons:
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            if is_hovered and not btn["hovered_last"]:
                self.audio.play_sound(setting.SoundEffect.MENU_HOVER_PATH)
            btn["hovered_last"] = is_hovered
            btn["hover"] = is_hovered

            target_scale = 1.1 if is_hovered else 1.0
            btn["scale"] += (target_scale - btn["scale"]) * 0.2

        # 無需切換場景時回傳 None
        return None

    # -------------------------------------------------------------
    # 畫面渲染
    # -------------------------------------------------------------
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        # 裝飾動畫
        self.animator1.draw(self.screen)
        self.animator2.draw(self.screen)

        # 標題
        title_surf = self.title_font.render(
            "Lazy Me Today Too", True, (142, 88, 51)
        )
        title_rect = title_surf.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)

        # 按鈕
        for btn in self.buttons:
            rect = btn["rect"]
            scaled_rect = pygame.Rect(
                0,
                0,
                int(rect.width * btn["scale"]),
                int(rect.height * btn["scale"]),
            )
            scaled_rect.center = rect.center

            base_color = (200, 200, 250) if btn["hover"] else (180, 180, 180)
            border_color = (120, 120, 160)
            pygame.draw.rect(self.screen, base_color, scaled_rect, border_radius=15)
            pygame.draw.rect(self.screen, border_color, scaled_rect, 3, border_radius=15)

            text_surf = self.subtitle_font.render(btn["text"], True, (50, 50, 50))
            text_rect = text_surf.get_rect(center=scaled_rect.center)
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    # -------------------------------------------------------------
    # 主循環
    # -------------------------------------------------------------
    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            result = self.update()
            if result is not None:
                return result
            self.draw()


