import pygame
import asyncio
import sys
from UI.components.base_scene import BaseScene, wrap_text
from UI.components.button import Button
import setting

class EventScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.background_img = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert()
        note_img = pygame.image.load(setting.ImagePath.EVENT_WINDOW_PATH).convert_alpha()
        orig_width, orig_height = note_img.get_size()
        target_width = 850
        scale_factor = target_width / orig_width
        target_height = int(orig_height * scale_factor)
        self.note_img = pygame.transform.smoothscale(note_img, (target_width, target_height))
        self.note_rect = self.note_img.get_rect(center=(600, 400))
        self.title_alpha = 0  # 標題淡入透明度
        self.title_alpha_speed = 20  # 每幀增加多少

        self.font = pygame.font.Font(setting.JFONT_PATH_BOLD, 36)
        self.title_font = pygame.font.Font(setting.HFONT_PATH,36)
        self.font_small = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)
        self.BUTTON_COLOR = (200, 180, 150)
        self.BUTTON_HOVER_COLOR = (255, 220, 180)
        self.BUTTON_TEXT_COLOR = (50, 30, 10)
        self.button_width = 545
        self.button_height = 70
        self.button_margin = 20
        self.max_text_width = self.button_width - 20

        self.has_sound = False

        self.title = self.player.week_data.get("title", "")

        if len(self.player.week_data["events"]) != 0:
            self.event_text = self.player.week_data["events"]["description"]

            self.options = []
            for key, option in self.player.week_data["events"]["options"].items():
                self.options.append((option["text"], key))
                
            # 計算按鈕初始位置
            self.buttons = []
            for i, (text, key) in enumerate(self.options):
                button_y = self.note_rect.centery - 30 + i * (self.button_height + self.button_margin)
                button = (Button(self.note_rect.centerx - 260, button_y,
                                self.button_width, self.button_height, key + "." + text, self.font_small,
                                self.BUTTON_COLOR, self.BUTTON_TEXT_COLOR, self.BUTTON_HOVER_COLOR), key)
                self.buttons.append(button)
    

        # 動畫屬性
        self.note_anim_x = -1000  # 從螢幕左外側開始
        self.note_target_x = self.note_rect.x
        self.animating_in = True

        

    def update(self):
        if self.animating_in:
            # 緩動滑入
            speed = 40
            if self.note_anim_x < self.note_target_x:
                self.note_anim_x += speed
                if self.note_anim_x >= self.note_target_x:
                    self.note_anim_x = self.note_target_x
                    self.animating_in = False
            return  # 動畫時不處理事件
        if len(self.player.week_data["events"]) == 0 :
            return "finished"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.buttons:
                if button[0].handle_event(event):
                    attribute = self.player.week_data["events"]["options"][button[1]]["attribute"]
                    
                    # 加分數之前先做紀錄
                    changes = {"study": 0, "social": 0, "play_game": 0, "rest": 0}

                    if "study" in attribute:
                        self.player.study(1)
                        changes["study"] += 1
                    if "social" in attribute:
                        self.player.socialize(1)
                        changes["social"] += 1
                    if "play_game" in attribute:
                        self.player.play_game(1)
                        changes["play_game"] += 1
                    if "rest" in attribute:
                        self.player.rest(1)
                        changes["rest"] += 1

                    self.player.chosen[self.player.week_number] = button[1]
                    print(f"你選擇了選項 {button[1]}: {button[0].text}")
                    event_text = self.event_text.replace('\n', '')
                    # ✅ 新增 event_history 記錄（使用 dict，key 為 week_number）
                    if self.player.week_number != 8 and self.player.week_number != 16 :
                            
                        self.player.event_history[self.player.week_number] = {
                        "event_text": event_text,
                        "option_text": self.player.week_data["events"]["options"][button[1]]["text"],
                        "changes": {
                            "mood": self.player.last_week_change[0],
                            "energy": self.player.last_week_change[1],
                            "social": self.player.last_week_change[2],
                            "knowledge": self.player.last_week_change[3]
                        }
                }
                    return "finished"


    def draw(self):
        if len(self.player.week_data["events"]) == 0 :
            return "finished"
        self.screen.blit(self.background_img, (0, 0))
        # 便條紙滑入
        note_rect_anim = self.note_rect.copy()

        note_rect_anim.x = int(self.note_anim_x)
        self.screen.blit(self.note_img, note_rect_anim)

        #print(pygame.mouse.get_pos())
    

        # 文字滑入
        lines = self.event_text.splitlines() if self.event_text else []
        # 文字根據 note_rect_anim.x 偏移
        text_offset_x = note_rect_anim.x - self.note_rect.x
        self.draw_lines(self.screen, lines, self.font, start_pos=(350 + text_offset_x, 240))
        
        
        # 畫標題
        title_surface = self.title_font.render(self.title, True, (60, 179, 133))
        # 建立一個有 alpha 的 surface
        title_alpha_surface = pygame.Surface(title_surface.get_size(), pygame.SRCALPHA)
        title_alpha_surface.blit(title_surface, (0, 0))
        title_alpha_surface.set_alpha(self.title_alpha)
        title_rect = title_surface.get_rect()
        title_rect.topleft = (350 + text_offset_x, 160)
        self.screen.blit(title_alpha_surface, title_rect)
        self.screen.blit(self.title_font.render(self.title, True, (60, 179, 133)), (350 + text_offset_x, 140))
        
        # 按鈕滑入
        for i, button in enumerate(self.buttons):
            btn = button[0]
            btn_x = btn.rect.x + text_offset_x
            btn_y = btn.rect.y
            btn.rect.topleft = (btn_x, btn_y)
            btn.draw(self.screen)
            # 恢復原本 x，避免 hover 判斷錯誤
            btn.rect.topleft = (btn_x - text_offset_x, btn_y)

    def draw_lines(self, surface, lines, font, start_pos=(360, 200), color=(0, 0, 0)):
        x, y = start_pos
        line_spacing = 10
        line_height = font.get_linesize()
        for line in lines:
            txt_surf = font.render(line, True, color)
            surface.blit(txt_surf, (x, y))
            y += line_height + line_spacing

    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            result = None
            result = self.update()
            if result is not None:
                print(f"Scene result: {result}")
                return result
                
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return None