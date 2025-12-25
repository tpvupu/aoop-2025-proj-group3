import pygame
from UI.components.base_scene import BaseScene, draw_wrapped_text
from UI.main_scene import MainScene
from UI.components.character_animator import CharacterAnimator
from UI.components.audio_manager import AudioManager
import setting
from UI.components.floating_emoji import FloatingEmoji

class EndScene(MainScene):
    def __init__(self, screen, player):
        super().__init__(screen, player)
        self.background = pygame.image.load(
            setting.ImagePath.BACKGROUND_PATH
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )
        self.background.set_alpha(100)
        
        self.player = player
        self.title_font = pygame.font.Font(
            setting.JFONT_PATH_BOLD, 54
        )
        self.subtitle_font = pygame.font.Font(
            setting.JFONT_PATH_REGULAR, 48
        )

        # ---------- 音樂 ----------    
        self.audio = AudioManager.get_instance()
        self.audio.play_bgm(setting.BGM.MITAO_HUIHUI_PATH)


        # ---------- 按鈕 ----------
        self.buttons = []
        button_texts = [
            ("重新開始", "RESTART"),
            ("顯示排行", "SHOW_RANK"),
            ("結果分析", "ADVICE"),
            ("回饋表單", "FEEDBACK"),
            ("退出遊戲", "QUIT"),
        ]
        button_w, button_h, spacing = 300, 70, 30
        total_h = len(button_texts) * (button_h + spacing) - spacing
        start_y = (self.SCREEN_HEIGHT - total_h) // 2 + 100

        for i, (text, action) in enumerate(button_texts):
            rect = pygame.Rect(
                (self.SCREEN_WIDTH - button_w) // 2 + 250,
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
        self.animator2 = CharacterAnimator(self.player.ending, (50, 400), (300, 300))
        
        self.animator2.frame_delay = 3
        # ---------- 其他 ----------
        self.selected_result = None

        # 表情圖初始化        
        self.emoji_paths = [
            setting.ImagePath.HAPPY_W_PATH,
            setting.ImagePath.KISS_W_PATH,
            setting.ImagePath.HEHE_W_PATH,
            setting.ImagePath.SAD_W_PATH,
            setting.ImagePath.ANGRY_W_PATH,
            setting.ImagePath.HEART_W_PATH,
            setting.ImagePath.LIGHTENING_W_PATH,
            setting.ImagePath.ROCKET_W_PATH
        ]

        self.floating_emoji_paths = [
            setting.ImagePath.HAPPY_PATH,
            setting.ImagePath.KISS_PATH,
            setting.ImagePath.HEHE_PATH,
            setting.ImagePath.SAD_PATH,
            setting.ImagePath.ANGRY_PATH,
            setting.ImagePath.HEART_PATH,
            setting.ImagePath.LIGHTENING_PATH,
            setting.ImagePath.ROCKET_PATH
        ]
        self.emoji_surfaces = [pygame.image.load(p).convert_alpha() for p in self.emoji_paths]
        self.emoji_surfaces = [pygame.transform.smoothscale(img, (90, 90)) for img in self.emoji_surfaces]
        self.emoji_rects = []
        self.emoji_clicked_frames = [0] * len(self.emoji_surfaces)  # 點擊動畫持續幀數
        self.emoji_frame_max = 3  # 點擊放大的持續幀數
        self.floating_emojis = []
        self.emoji_mask = [pygame.mask.from_surface(img) for img in self.emoji_surfaces]
        self.floating_emoji_surfaces = [pygame.image.load(p).convert_alpha() for p in self.floating_emoji_paths]


    # -------------------------------------------------------------
    # 更新邏輯 & 事件處理
    # -------------------------------------------------------------

    def draw_emoji(self):
        self.emoji_rects = []

        # 表情符號座標
        left_start_x = 30
        left_y = self.SCREEN_HEIGHT - 120

        for i, emoji in enumerate(self.emoji_surfaces):
            # 計算位置        
            x = left_start_x + i * 70
            y = left_y

            rect = emoji.get_rect(topleft=(x, y))
            self.emoji_rects.append(rect)

            # 根據是否在點擊動畫狀態進行放大
            if self.emoji_clicked_frames[i] > 0:
                scale = 1.2
                self.emoji_clicked_frames[i] -= 1
            else:
                scale = 1.0

            new_size = int(90 * scale)
            scaled_img = pygame.transform.smoothscale(self.emoji_surfaces[i], (new_size, new_size))
            new_rect = scaled_img.get_rect(center=rect.center)
            self.screen.blit(scaled_img, new_rect.topleft)
        
        # 畫出所有飄移表情
        for emoji in self.floating_emojis:
            emoji.draw(self.screen)


    # -------------------------------------------------------------
    # 畫面渲染
    # -------------------------------------------------------------
    def draw_player_stats(self):

        stats_bg = pygame.Surface((480, 250), pygame.SRCALPHA)
        stats_bg.fill((255, 255, 255, 180))  # 180 可調整透明度，0~255

        # 貼到主畫面
        self.screen.blit(stats_bg, (20, 50))

        # 畫邊框
        pygame.draw.rect(self.screen, (100, 100, 100), (20, 50, 480, 250), 2)

        stats = {
            "intelligence": self.player.intelligence,
            "mood": self.player.mood,
            "energy": self.player.energy,
            "social": self.player.social,
            "knowledge": self.player.knowledge
        }

        font = self.stats_font
        x_left = 30
        x_right = x_left + self.bar_width + 80
        y_start = 180
        bar_height = self.bar_height
        bar_width = self.bar_width
        gap_y = self.bar_gap
        label_offset = -5  # 調整文字與條的對齊

        # 印出玩家的頭像
        player_imaage = pygame.image.load(self.player.header).convert_alpha()
        player_image = pygame.transform.smoothscale(player_imaage, (100, 100))
        player_rect = player_image.get_rect(topleft=(40, 60))
        self.screen.blit(player_image, player_rect)
        # 印出玩家的名字
        name_label = font.render(self.player.chname + " " + self.player.name, True, (0, 0, 0))
        name_rect = name_label.get_rect(topleft=(160, 80))
        self.screen.blit(name_label, name_rect)
        # 印出玩家的週數
        week_label = font.render("Final Result", True, (0, 0, 0))
        week_rect = week_label.get_rect(topleft=(160, 120))
        self.screen.blit(week_label, week_rect)

        # 第一排：intelligence / mood
        for i, key in enumerate(["intelligence", "mood"]):
            x = x_left if i == 0 else x_right
            y = y_start
            fill = max(0, min(1, stats[key] / 100))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, self.bar_colors[key], (x + 65, y, int(bar_width * fill), bar_height))
            label = font.render(f"智力 {self.player.intelligence}" if key == "intelligence" else f"心情 {self.player.mood}", True, (0, 0, 0))
            self.screen.blit(label, (x, y + label_offset))

        # 第二排：energy / social
        for i, key in enumerate(["energy", "social"]):
            x = x_left if i == 0 else x_right
            y = y_start + bar_height + gap_y +10
            fill = max(0, min(1, stats[key] / 100))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, self.bar_colors[key], (x + 65, y, int(bar_width * fill), bar_height))
            label = font.render(f"體力 {self.player.energy}" if key == "energy" else f"社交 {self.player.social}", True, (0, 0, 0))
            self.screen.blit(label, (x, y + label_offset))
        
        # 第三排：knowledge（橫跨兩個 bar）
        y = y_start + 2 * (bar_height + gap_y) + 20
        x = x_left
        total_width = (x_right - x_left) + 130 + bar_width  # 橫跨兩欄
        fill = max(0, min(1, stats["knowledge"] / 100))
        pygame.draw.rect(self.screen, (200, 200, 200), (x + 65, y, total_width - 130, bar_height), 2)
        pygame.draw.rect(self.screen, self.bar_colors["knowledge"], (x + 65, y, int((total_width - 130) * fill), bar_height))
        label = font.render(f"知識 {self.player.knowledge:.0f}/100", True, (0, 0, 0))
        self.screen.blit(label, (x, y + label_offset))

        # 印出玩家的總成績
        font2 = pygame.font.Font(setting.JFONT_PATH_Light, 22)
        text0 = font2.render(f"GPA: {self.player.GPA}", True, (0, 0, 0))
        text0_rect = text0.get_rect(topleft=(x_right + 60, 65))
        self.screen.blit(text0, text0_rect)
        # 印出總成績
        text01 = font2.render(f"Total Score: {self.player.total_score}", True, (0, 0, 0))
        text01_rect = text0.get_rect(topleft=(x_right + 60, 90))
        self.screen.blit(text01, text01_rect)
        #  印出期中考和期末考成績
        text1 = font2.render(f"Midterm: {self.player.midterm}", True, (0, 0, 0))
        text1_rect = text1.get_rect(topleft=(x_right + 60, 115))
        self.screen.blit(text1, text1_rect)
        text2 = font2.render(f"Final: {self.player.final}", True, (0, 0, 0))
        text2_rect = text2.get_rect(topleft=(x_right + 60, 140))
        self.screen.blit(text2, text2_rect)

    


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.draw_player_stats()
        # 裝飾動畫
        self.animator2.draw(self.screen)
        self.draw_emoji()

        # 標題
        title_surf = self.title_font.render(
            f"Congratulation!!", True, (50, 50, 50)
        )
        title_rect = title_surf.get_rect(center=(self.SCREEN_WIDTH // 2 + 200, 70))
        self.screen.blit(title_surf, title_rect)

        # 印出玩家的GPA
        gpa_surf = self.subtitle_font.render(
            f"{self.player.name}'s Final GPA：{self.player.GPA:.2f}", True, (50, 50, 50)
        )
        gpa_rect = gpa_surf.get_rect(center=(self.SCREEN_WIDTH // 2 + 200, 150))
        self.screen.blit(gpa_surf, gpa_rect)

        # 副標題
        subtitle_surf = self.subtitle_font.render(
            f"期中考：{self.player.midterm}, 期末考：{self.player.final}", True, (50, 50, 50)
        )
        subtitle_rect = subtitle_surf.get_rect(center=(self.SCREEN_WIDTH // 2 + 200 , 200))
        self.screen.blit(subtitle_surf, subtitle_rect)


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


        # diary icon hover 放大
        if self.player.week_number != 0:
            if self.diary_hover:
                scaled = pygame.transform.scale(self.diary_icon, (100, 100))
                rect = scaled.get_rect(center=self.diary_rect.center)
                self.screen.blit(scaled, rect.topleft)
            else:
                self.screen.blit(self.diary_icon, self.diary_rect.topleft)

        pygame.display.flip()

    # -------------------------------------------------------------
    # 主循環
    # -------------------------------------------------------------
    def update(self):
        self.clock.tick(self.FPS)
        self.animator2.update()
        # 按鈕 hover 更新
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            if is_hovered and not btn["hovered_last"]:
                self.audio.play_sound(setting.SoundEffect.BO_PATH)
            btn["hovered_last"] = is_hovered
            btn["hover"] = is_hovered
            target_scale = 1.1 if is_hovered else 1.0
            btn["scale"] += (target_scale - btn["scale"]) * 0.2
        # update 飄浮 emoji
        for emoji in self.floating_emojis:
            emoji.update()
        # 無需切換場景時回傳 None
        
        # 在 update() 裡
        if self.diary_rect.collidepoint(mouse_pos):
            if not self.diary_hover:
                self.audio.play_sound(setting.SoundEffect.MENU_HOVER_PATH)
                self.diary_hover = True
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                return "DIARY"
        else:
            self.diary_hover = False
        return None

    def run(self):
        self.running = True
        if self.audio.is_sound_playing(setting.SoundEffect.CHEER_CHEER_PATH):
            self.audio.stop_sound(setting.SoundEffect.CHEER_CHEER_PATH)
        self.audio.play_sound(setting.SoundEffect.CHEER_CHEER_PATH)
        while self.running:
            result = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    # 按鈕
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            return btn["action"]
                    # emoji
                    for i, rect in enumerate(self.emoji_rects):
                        if rect.collidepoint(mouse_pos):
                            rel_x = mouse_pos[0] - rect.left
                            rel_y = mouse_pos[1] - rect.top
                            if 0 <= rel_x < rect.width and 0 <= rel_y < rect.height:
                                if self.emoji_mask[i].get_at((rel_x, rel_y)):
                                    self.audio.play_sound(setting.SoundEffect.MENU_HOVER_PATH)
                                    self.emoji_clicked_frames[i] = self.emoji_frame_max
                                    float_img = pygame.transform.smoothscale(self.floating_emoji_surfaces[i], (90, 90))
                                    float_start = rect.center
                                    floating = FloatingEmoji(float_img, float_start)
                                    self.floating_emojis.append(floating)

                
                
            if self.update() ==  "DIARY":
                return "DIARY"
            # 更新動畫和按鈕狀態
            self.draw()
            # result 只會由按鈕點擊回傳
