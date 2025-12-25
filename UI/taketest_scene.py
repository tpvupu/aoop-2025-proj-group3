import pygame
from UI.components.base_scene import BaseScene
from UI.components.character_animator import CharacterAnimator
import setting

class TakeTestScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.titlefont = pygame.font.Font(setting.JFONT_PATH_BOLD, 54)
        self.font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 36)
        self.player = player
        self.audio.fade_out_bgm(1000)  # 淡出背景音樂
        self.audio.play_bgm(setting.BGM.DRUMDRUM_PATH)  # 播放考試背景音樂

        # 背景與透明遮罩
        self.background = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
        self.overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay_alpha = 0

        if player.week_number == 8:
            self.test_type = "期中考"
        else:
            self.test_type = "期末考"

        # 文字敘述
        self.text_lines = f"{self.player.chname} 同學，你已經準備好進行{self.test_type}試了嗎？"
        self.animator = CharacterAnimator(self.player.testing, (850, 400), (300, 300))
        self.animator.frame_delay = 20  # 控制動畫速度

    def update(self):
        self.animator.update()
        # 透明遮罩淡入
        if self.overlay_alpha < 255:
            self.overlay_alpha = min(255, self.overlay_alpha + 5)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        self.screen.blit(self.overlay_surface, (0, 0))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.animator.draw(screen)

        # 顯示文字
        text_surface = self.titlefont.render(self.text_lines, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        screen.blit(text_surface, text_rect)
        # 顯示提示文字
        prompt_surface = self.font.render("按下 Enter 鍵開始考試", True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        screen.blit(prompt_surface, prompt_rect)

    def run(self):
        if self.player.week_number ==8 or self.player.week_number == 16:
                        self.player.event_history[self.player.week_number] = {
                            "event_text": "",
                            "option_text": "",
                            "changes": {
                            }
                        }

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.audio.play_sound(setting.SoundEffect.DONGDONG_PATH)
                          # 播放按下 Enter 音效
                        # 按下 Enter 鍵後，切到 GradingScene
                        # 延遲一段時間以模擬考試過程
                        pygame.time.delay(500)  # 模擬考試過程
                        self.running = False
                        grade_scene = GradingScene(self.screen, self.player)
                        result = grade_scene.run()
                        self.running = False  # 確保當 GradingScene 結束後，這個場景也結束
                        return result

                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw(self.screen)
            pygame.display.update()



class GradingScene(BaseScene):
    def __init__(self, screen, player):
        super().__init__(screen)
        self.titlefont = pygame.font.Font(setting.JFONT_PATH_BOLD, 54)
        self.font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 36)
        self.player = player
        self.audio.fade_out_bgm(5000)
        self.audio.play_sound_loop(setting.SoundEffect.SMALL_DRUM_PATH)

        # 背景與透明遮罩
        self.background = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
        self.overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay_alpha = 0

        self.animator = CharacterAnimator(self.player.taketest, (850, 400), (300, 300))
        self.animator.frame_delay = 20  # 控制動畫速度

        if player.week_number == 8:
            player.get_midterm()
            self.score = player.midterm
            self.score_type = "期中考"
        else:
            player.get_final()
            self.score = player.final
            self.score_type = "期末考"

        # 文字敘述
        self.text_lines = f"{self.player.chname} 同學，你的{self.score_type}成績是 "
        self.displayed_score = 0
        self.reveal_speed = max(1, int(abs(self.score) // 100))  # 跳分速度
        self.show_full_score = False
        self.frame_count = 0

        self.ending_anim_switch = False  # 用於控制是否顯示結束動畫

    def update(self):
        self.animator.update()
        # 透明遮罩淡入
        if self.overlay_alpha < 255:
            self.overlay_alpha = min(255, self.overlay_alpha + 5)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        self.screen.blit(self.overlay_surface, (0, 0))
        # 跳分動畫
        if not self.show_full_score:
            self.frame_count += 1
            if self.frame_count % 10 == 0:  # 每3幀才加一次分數，數字越大越慢
                if self.displayed_score < int(self.score):
                    self.displayed_score += self.reveal_speed
                    # 新增：分數大於75且還沒切換動畫時，切換到結束動畫
                    if self.displayed_score >= 70 and not self.ending_anim_switch:
                        self.animator.switch_animation(self.player.ending)
                        if self.audio.is_sound_playing(setting.SoundEffect.CHEER_CHEER_PATH):
                            self.audio.stop_sound(setting.SoundEffect.CHEER_CHEER_PATH)
                        self.audio.play_sound(setting.SoundEffect.CHEER_CHEER_PATH)
                        self.ending_anim_switch = True  # 切換動畫後設置為 True")
                    if self.displayed_score >= int(self.score):
                        self.displayed_score = int(self.score)
                        self.audio.play_sound(setting.SoundEffect.BLING_PATH)  # 播放成績完成音效
                else: 
                    self.show_full_score = True                    
                    # 淡入恢復背景音樂
                    self.audio.stop_sound(setting.SoundEffect.SMALL_DRUM_PATH)  # 停止跳分音效
                    self.audio.play_bgm(setting.BGM.MITAO_HUIHUI_PATH, loop=-1)
                    
        
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.animator.draw(screen)
        # 顯示文字
        score_text = f"{self.text_lines}{self.displayed_score if not self.show_full_score else self.score:.2f} 分！"
        text_surface = self.titlefont.render(score_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        screen.blit(text_surface, text_rect)

        # 顯示提示文字
        if self.show_full_score:
            prompt_surface = self.font.render("點擊以退出", True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 350))
            screen.blit(prompt_surface, prompt_rect)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if self.show_full_score and event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
                    return self.score  # 返回分數以便後續使用
                if event.type == pygame.QUIT:
                    self.running = False
            

            self.update()
            self.draw(self.screen)
            pygame.display.update()