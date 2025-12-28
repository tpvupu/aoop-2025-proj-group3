import pygame
import asyncio
import sys
import json
from UI.components.base_scene import BaseScene
from UI.lucky_wheel_scene import LuckyWheelScene
from UI.components.character_animator import CharacterAnimator
from UI.taketest_scene import TakeTestScene
from UI.end_scene import EndScene
import setting

class StoryScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)

        self.player = player

        self.title_font = pygame.font.Font(setting.JFONT_PATH_BOLD, 48)
        self.font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 36)
        
        self.animator = CharacterAnimator(player.storytyping, (900, 50), (220, 200))

        self.title_alpha = 0  # 標題淡入透明度
        self.title_alpha_speed = 20  # 每幀增加多少

        self.background = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.background.set_alpha(65)


        self.char_interval = 120  # 字母出現間隔（毫秒）
        self.line_spacing = 10
        self.line_height = self.font.get_linesize()

        intro_text = self.player.week_data.get("intro", "")
        self.lines = intro_text.splitlines() if intro_text else []
        self.title = self.player.week_data.get("title", "")

        self.current_line = 0
        self.current_char = 0
        self.displayed_lines = []
        self.last_char_time = pygame.time.get_ticks()
        self.all_finished = False
        self.running = True

        # 開始打字音效
        self.audio.play_sound(setting.SoundEffect.TYPING_PATH)  # 迴圈播放

                

  

    def update(self):
        #print(pygame.mouse.get_pos())
        if self.title_alpha < 255:
            self.title_alpha = min(255, self.title_alpha + self.title_alpha_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if self.all_finished:
                    self.running = False  # 點擊結束故事
                else:
                    # 把剩下的文字一次顯示出來
                    while self.current_line < len(self.lines):
                        self.displayed_lines.append(self.lines[self.current_line])
                        self.current_line += 1
                    self.all_finished = True
                    self.audio.stop_sound(setting.SoundEffect.TYPING_PATH)

                
            
        self.animator.update()  # 更新動畫
        now = pygame.time.get_ticks()

        if not self.all_finished and now - self.last_char_time > self.char_interval:
            self.last_char_time = now
            self.current_char += 1
            if self.current_char > len(self.lines[self.current_line]):
                self.displayed_lines.append(self.lines[self.current_line])
                self.current_line += 1
                self.current_char = 0
                if self.current_line >= len(self.lines):
                    self.all_finished = True
                    self.audio.stop_sound(setting.SoundEffect.TYPING_PATH)


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.animator.draw(self.screen)

        # 假設左右邊距 40，上方起始高度 160
        left_margin = 100
        top_start = 230

        # 畫標題（淡入）
        if self.title:
            title_surface = self.title_font.render(self.title, True, (50, 50, 50))
            # 建立一個有 alpha 的 surface
            title_alpha_surface = pygame.Surface(title_surface.get_size(), pygame.SRCALPHA)
            title_alpha_surface.blit(title_surface, (0, 0))
            title_alpha_surface.set_alpha(self.title_alpha)
            title_rect = title_surface.get_rect()
            title_rect.topleft = (left_margin-30, 120)
            self.screen.blit(title_alpha_surface, title_rect)

        # 畫分隔線（淡入）
        line_width = self.screen.get_width() - left_margin - left_margin - 200
        line_surface = pygame.Surface((line_width, 2), pygame.SRCALPHA)
        pygame.draw.line(line_surface, (100, 100, 100, self.title_alpha), (0, 1), (line_width, 1), 2)
        self.screen.blit(line_surface, (left_margin-50, 180))

        # 已顯示的完整行
        y = top_start
        for line in self.displayed_lines:
            text_surface = self.font.render(line, True, (50, 50, 50))
            self.screen.blit(text_surface, (left_margin, y))
            y += self.line_height + self.line_spacing

        # 當前行正在打字的部分
        if not self.all_finished and self.current_line < len(self.lines):
            partial_text = self.lines[self.current_line][:self.current_char]
            text_surface = self.font.render(partial_text, True, (50, 50, 50))
            self.screen.blit(text_surface, (left_margin, y))
            if self.audio.is_sound_playing(setting.SoundEffect.TYPING_PATH) is False:
                self.audio.play_sound(setting.SoundEffect.TYPING_PATH)
                

    
        tip = self.font.render("（點擊以結束）", True, (150, 150, 150))
        # 水平置中，垂直位置在文字區底部+50
        self.screen.blit(tip, (self.screen.get_width() // 2 - tip.get_width() // 2, 630))
        
    async def run(self):
        
        while self.running:
            await asyncio.sleep(0)
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        if self.player.week_number == 3:
            options = ["超可愛學姐\n帥潮學長", "看起來是系邊\n有點宅宅的學長", "超搞笑的系核\n第一次見面\n就表演倒立走路", "卷哥卷姐", "被放生了"]
            lucky_scene = LuckyWheelScene(self.screen, options)
            result = lucky_scene.run()
            self.player.home =  result

        # 期中考
        if self.player.week_number == 8:
            taketest_scene = TakeTestScene(self.screen, self.player)
            self.player.midterm = taketest_scene.run()


        # 期末考
        if self.player.week_number == 16: 
            taketest_scene = TakeTestScene(self.screen, self.player)
            self.player.final = taketest_scene.run()
            options = ["幸運教授指數3", "幸運教授指數5", "幸運教授指數4"]
            lucky_scene = LuckyWheelScene(self.screen, options)
            result = lucky_scene.run()
            # 結果是分別對應 3, 5, 4
            if result == "幸運教授指數3":
                result = 3
            elif result == "幸運教授指數5":
                result = 5
            elif result == "幸運教授指數4":
                result = 4
            self.player.lucky_prof = result
            
                    
            
        
        
