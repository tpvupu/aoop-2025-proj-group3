import pygame
from UI.components.base_scene import BaseScene, draw_wrapped_text
from UI.components.image_button import ImageButton
import setting

class DiaryScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.diary_img = pygame.image.load("resource/image/diary_image.png").convert_alpha()
        self.diary_img = pygame.transform.smoothscale(self.diary_img, (1200, 1100))
        self.diary_rect = self.diary_img.get_rect(center=(610, 450))
        self.text_rect = pygame.Rect(150, 60, 900, 600)
        self.font = pygame.font.Font(setting.JFONT_PATH_REGULAR,32)
        
        self.week_index = self.player.week_number - 1
        self.animator = self.player.gif_choose(self.week_index+1,(850, 450), (200, 200))
        self.total_weeks = len(self.player.event_history)
        self.btn_left = ImageButton("resource/image/left.png", (100, 700), size=(80, 80))
        self.btn_right = ImageButton("resource/image/right.png", (980, 700), size=(80, 80))
        self.btn_back = ImageButton("resource/image/back.png", (90, 20), size=(100, 100))
        # Advice toggle
        self.advice_text = None
        # reference player's persisted weekly advice
        self.advice_by_week = self.player.weekly_advice
        self.advice_font = pygame.font.Font(setting.JFONT_PATH_Light, 28)
        self.advice_hint = pygame.font.Font(setting.JFONT_PATH_REGULAR, 24).render("按 A 生成本週建議", True, (60, 60, 60))
        self.advice_hint_rect = self.advice_hint.get_rect(topleft=(160, 680))

        # if there is prior advice for the current week, display it immediately
        if self.player.event_history:
            sorted_weeks = sorted(self.player.event_history.keys())
            if 0 <= self.week_index < len(sorted_weeks):
                cur_week = sorted_weeks[self.week_index]
                self.advice_text = self.advice_by_week.get(cur_week)

    def draw(self):
        
        self.screen.fill((245, 240, 225))  # 柔和米白色
        self.screen.blit(self.diary_img, self.diary_rect)

        if self.player.event_history:
            sorted_weeks = sorted(self.player.event_history.keys())
            if 0 <= self.week_index < len(sorted_weeks):
                week = sorted_weeks[self.week_index]
                entry = self.player.event_history.get(week)
                event_text = entry.get("event_text", "")
                option_text = entry.get("option_text", "")
                changes = entry.get("changes", {})
                if week == 8:
                    content = f"第 {week} 週回顧\n這週是你的期中考，恭喜{self.player.chname}考完啦~\n你的分數：{self.player.midterm}"
                elif week == 16:
                    content = f"第 {week} 週回顧\n這週是你的期末考，恭喜{self.player.chname}考完啦~\n你的分數：{self.player.final}"
                else:   
                    content = f"第 {week} 週回顧\n事件內容：{event_text}\n你的選擇：{option_text}\n狀態變化："
                    for attr, value in changes.items():
                        if value > 0:
                            content += f"{attr} +{value}  "
                        elif value < 0:
                            content += f"{attr} {value}  "
                    content += (
                        f"\n本週狀態：心情 {self.player.mood}  "
                        f"體力 {self.player.energy}  "
                        f"社交 {self.player.social}  "
                        f"知識 {self.player.knowledge:.0f}"
                    )
                draw_wrapped_text(self.screen, content, self.font, self.text_rect, (50,30,30),48)
        # Advice block
        if self.advice_text:
            advice_rect = pygame.Rect(150, 420, 900, 300)
            draw_wrapped_text(self.screen, "AI 建議：\n" + self.advice_text, self.advice_font, advice_rect, (20,20,70), 36)
        else:
            self.screen.blit(self.advice_hint, self.advice_hint_rect)
        self.animator.draw(self.screen)
        self.btn_left.draw(self.screen)
        self.btn_right.draw(self.screen)
        self.btn_back.draw(self.screen)

    def run(self):
        while self.running:
            self.animator.update()
            self.btn_left.update()
            self.btn_right.update()
            self.btn_back.update()

            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_left.rect.collidepoint(event.pos):
                        self.week_index = max(0, self.week_index - 1)
                        sorted_weeks = sorted(self.player.event_history.keys())
                        prev_week = sorted_weeks[self.week_index] if sorted_weeks else None
                        self.advice_text = self.advice_by_week.get(prev_week)
                        self.animator = self.player.gif_choose(self.week_index+1, (850, 450), (200, 200))
                    elif self.btn_right.rect.collidepoint(event.pos):
                        self.week_index = min(self.total_weeks - 1, self.week_index + 1)
                        sorted_weeks = sorted(self.player.event_history.keys())
                        next_week = sorted_weeks[self.week_index] if sorted_weeks else None
                        self.advice_text = self.advice_by_week.get(next_week)
                        self.animator = self.player.gif_choose(self.week_index+1, (850, 450), (200, 200))
                    elif self.btn_back.rect.collidepoint(event.pos):
                        return "BACK"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    # Lazy import to avoid overhead in gameplay loop
                    try:
                        from services.feedback_generator import generate_weekly_advice
                        sorted_weeks = sorted(self.player.event_history.keys())
                        if 0 <= self.week_index < len(sorted_weeks):
                            week = sorted_weeks[self.week_index]
                            advice = generate_weekly_advice(self.player, week)
                            # stored in player by generator, keep local view in sync
                            self.advice_by_week[week] = advice
                            self.advice_text = advice
                    except Exception as _:
                        self.advice_text = "(產生建議失敗，請稍後再試或檢查網路/API 設定)"
        return None