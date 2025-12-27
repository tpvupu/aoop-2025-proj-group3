import pygame
from UI.components.character_animator import CharacterAnimator
from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager
from AI.simulation import Simulation
from character import Bubu, Yier, Mitao, Huihui
import setting

class RankScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.audio = AudioManager.get_instance()
        self.player = player
        # 背景
        self.background = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
        self.transition_direction = 1 

        self.overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay_alpha = 0 

        # 字型
        self.font_desc = pygame.font.Font(setting.JFONT_PATH_REGULAR, 36)

        # 動畫角色
        self.animator = CharacterAnimator(self.player.ending, (900, 30), (240, 220))
        self.animator.frame_delay = 5

        # 根據玩家角色類別來決定要用哪個角色類進行對比
        char_class_map = {
            'Bubu': Bubu,
            'Yier': Yier,
            'Mitao': Mitao,
            'Huihui': Huihui,
        }
        player_char_class = char_class_map.get(self.player.name, Bubu)

        # 執行兩個模擬：全部角色 + 該角色專用
        self.simulation = Simulation()
        self.simulation.run_and_plot_all_with_player(player)
        self.simulation.run_character_simulation_with_player(player, player_char_class)

        # 圖片載入與縮放
        # 全角色圖表
        self.all_images = []
        import os
        all_image_paths = [
            os.path.join(setting.SIMULATION_PLOTS_DIR, 'gpa_highlight.png'),
            os.path.join(setting.SIMULATION_PLOTS_DIR, 'total_highlight.png'),
            os.path.join(setting.SIMULATION_PLOTS_DIR, 'midterm_final_highlight.png'),
        ]
        for path in all_image_paths:
            img = pygame.image.load(path).convert_alpha()
            orig_w, orig_h = img.get_size()
            scale_ratio = min(800 / orig_w, 600 / orig_h)
            new_size = (int(orig_w * scale_ratio), int(orig_h * scale_ratio))
            scaled = pygame.transform.smoothscale(img, new_size)
            self.all_images.append(scaled)
        
        # 角色專用圖表
        self.character_images = []
        from pathlib import Path
        char_out_dir = Path(self.simulation.out_dir) / f"{player_char_class.__name__}_comparison"
        char_image_names = ['gpa_highlight.png', 'total_highlight.png', 'midterm_final_highlight.png']
        for img_name in char_image_names:
            img_path = char_out_dir / img_name
            try:
                img = pygame.image.load(str(img_path)).convert_alpha()
                orig_w, orig_h = img.get_size()
                scale_ratio = min(800 / orig_w, 600 / orig_h)
                new_size = (int(orig_w * scale_ratio), int(orig_h * scale_ratio))
                scaled = pygame.transform.smoothscale(img, new_size)
                self.character_images.append(scaled)
            except Exception as e:
                print(f"警告：無法載入圖表 {img_path}: {e}")
                blank = pygame.Surface((800, 600))
                blank.fill((50, 50, 50))
                self.character_images.append(blank)

        # 小號字體供按鈕使用
        self.font_button = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)
        
        self.current_page = 0
        self.next_page = None
        self.mode = "all"  # "all" 或 "character"

        # 滑動動畫參數
        self.transitioning = False
        self.slide_offset = 0
        self.slide_speed = 40  # 每 frame 移動速度

        # 自動換頁計時器
        self.page_timer = 0
        self.auto_page_delay = 5000  # 毫秒

    def update(self):
        if self.overlay_alpha < 140:
            self.overlay_alpha += 5
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))

        self.animator.update()
        self.page_timer += self.clock.get_time()

        if self.page_timer >= self.auto_page_delay and not self.transitioning:
            self.start_transition()

        if self.transitioning:
            self.slide_offset += self.slide_speed
            current_images = self.all_images if self.mode == "all" else self.character_images
            if self.slide_offset >= current_images[0].get_height():
                self.current_page = self.next_page
                self.transitioning = False
                self.slide_offset = 0
                self.page_timer = 0  # 重設計時器
    
    def start_transition(self, direction=1):
        self.transition_direction = direction
        current_images = self.all_images if self.mode == "all" else self.character_images
        self.next_page = (self.current_page + direction) % len(current_images)
        self.transitioning = True
        self.slide_offset = 0
        self.page_timer = 0
        self.audio.play_sound(setting.SoundEffect.NEXT_PAGE_PATH)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.overlay_surface, (0, 0))

        current_images = self.all_images if self.mode == "all" else self.character_images
        
        # 左邊主圖表區域
        img_current = current_images[self.current_page]
        rect_current = img_current.get_rect(center=(420, self.SCREEN_HEIGHT // 2 - self.slide_offset))
        screen.blit(img_current, rect_current)

        if self.transitioning:
            img_next = current_images[self.next_page]
            if self.transition_direction == 1:
                # 向下滑
                rect_next = img_next.get_rect(center=(420, self.SCREEN_HEIGHT // 2 + img_next.get_height() - self.slide_offset))
                rect_current = img_current.get_rect(center=(420, self.SCREEN_HEIGHT // 2 - self.slide_offset))
            else:
                # 向上滑
                rect_next = img_next.get_rect(center=(420, self.SCREEN_HEIGHT // 2 - img_next.get_height() + self.slide_offset))
                rect_current = img_current.get_rect(center=(420, self.SCREEN_HEIGHT // 2 + self.slide_offset))
            screen.blit(img_current, rect_current)
            screen.blit(img_next, rect_next)
        else:
            rect_current = img_current.get_rect(center=(420, self.SCREEN_HEIGHT // 2))
            screen.blit(img_current, rect_current)

        # 右邊切換面板
        panel_x = self.SCREEN_WIDTH - 360
        panel_y = 300
        panel_width = 280
        panel_height = 420
        
        # 背景面板
        pygame.draw.rect(screen, (170, 170, 170), (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)
        
        # 按鈕 1: 全角色
        button1_rect = pygame.Rect(panel_x + 15, panel_y + 40, panel_width - 30, 100)
        button1_color = (100, 150, 200) if self.mode == "all" else (60, 80, 100)
        pygame.draw.rect(screen, button1_color, button1_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 200, 255) if self.mode == "all" else (80, 100, 120), button1_rect, 2, border_radius=8)
        
        all_text = self.font_button.render("全角色排名", True, (230, 230, 230))
        screen.blit(all_text, (button1_rect.centerx - all_text.get_width()//2, button1_rect.centery - all_text.get_height()//2))
        
        # 按鈕 2: 該角色專用
        button2_rect = pygame.Rect(panel_x + 15, panel_y + 165, panel_width - 30, 100)
        button2_color = (100, 150, 200) if self.mode == "character" else (60, 80, 100)
        pygame.draw.rect(screen, button2_color, button2_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 200, 255) if self.mode == "character" else (80, 100, 120), button2_rect, 2, border_radius=8)
        
        char_text = self.font_button.render(f"{self.player.name}專屬排名", True, (230, 230, 230))
    
        screen.blit(char_text, (button2_rect.centerx - char_text.get_width()//2, button2_rect.centery - char_text.get_height()//2))
        
        # 頁碼指示
        page_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 24)
        page_text = page_font.render(f"{self.current_page + 1}/3", True, (40, 40, 40))
        screen.blit(page_text, (panel_x + panel_width//2 - page_text.get_width()//2, panel_y + 290))
        
        # 提示文字
        hint_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 22)
        hint1 = hint_font.render("↓ 下一頁", True, (40,40,40))
        hint2 = hint_font.render("↑ 上一頁", True, (40, 40, 40))
        hint3 = hint_font.render("Esc 退出", True, (40, 40, 40))
        screen.blit(hint1, (panel_x + 100, panel_y + 330))
        screen.blit(hint2, (panel_x + 100, panel_y + 360))
        screen.blit(hint3, (panel_x + 115, panel_y + 390))
        
        # 儲存按鈕矩形供事件處理使用
        self.button1_rect = button1_rect
        self.button2_rect = button2_rect

        self.animator.draw(screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_DOWN and not self.transitioning:
                self.start_transition(direction=1)
            elif event.key == pygame.K_UP and not self.transitioning:
                self.start_transition(direction=-1)
            elif event.key == pygame.K_1:  # 快速鍵：按 1 切換到全角色
                if self.mode != "all":
                    self.mode = "all"
                    self.page_timer = 0
            elif event.key == pygame.K_2:  # 快速鍵：按 2 切換到該角色專用
                if self.mode != "character":
                    self.mode = "character"
                    self.page_timer = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hasattr(self, 'button1_rect') and self.button1_rect.collidepoint(event.pos):
                if self.mode != "all":
                    self.mode = "all"
                    self.page_timer = 0
                    self.audio.play_sound(setting.SoundEffect.NEXT_PAGE_PATH)
            elif hasattr(self, 'button2_rect') and self.button2_rect.collidepoint(event.pos):
                if self.mode != "character":
                    self.mode = "character"
                    self.page_timer = 0
                    self.audio.play_sound(setting.SoundEffect.NEXT_PAGE_PATH)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.FPS)

        self.running = False
