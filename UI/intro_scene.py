import pygame
from UI.components.character_animator import CharacterAnimator
from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager
import setting
import asyncio

class IntroScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)
        
        # 背景與透明遮罩
        self.background = pygame.image.load(setting.ImagePath.BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)
        self.overlay_surface = pygame.Surface(screen.get_size()).convert_alpha()
        self.overlay_alpha = 0

        # 字型設定
        self.font = pygame.font.Font(setting.JFONT_PATH_BOLD, 36)
        self.font_desc = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)

        self.text_lines = [
            "歡迎來到模擬人生大學版",
            "在這裡，你的每一週都充滿未知挑戰與選擇",
            "你會選擇耍廢？還是成為人生勝利組？",
            "遊戲中的每一步選擇都將影響你的角色發展",
            "在這個遊戲中，你將有四個角色可以選!",
            "從課業到社交，從挑戰到成就，每一週都是新的冒險",
            "按下Enter並點選開始遊戲選擇跟你最像的角色吧!"
        ]
        self.line_index = 0            # 目前正在顯示哪一行
        self.char_index = 0            # 該行目前顯示到第幾個字
        self.reveal_lines = []         # 每一行目前顯示的內容
        self.frame_count = 0             # 用於控制打字速度
        self.type_speed = 3             # 控制打字速度，數字越小越快
        for _ in self.text_lines:
            self.reveal_lines.append("")


        # 動畫角色
        self.animator = CharacterAnimator(setting.GIF_PATHS['YIER_PLAY_GAME_FRAMES'], (900, 50), (240, 220))
        self.animator.frame_delay = 3  # 控制動畫速度

        
    async def run(self):
        self.running = True
        while self.running:
            await asyncio.sleep(0)
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw(self.screen)
            pygame.display.update()

        self.audio.stop_sound(setting.SoundEffect.TYPING_PATH)  # 保險：離開場景時也停止打字音效


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.line_index >= len(self.text_lines):
                    self.audio.stop_sound(setting.SoundEffect.TYPING_PATH)
                    self.running = False
                else:
                    # 還沒打完就強制顯示完畢
                    self.reveal_lines = self.text_lines.copy()
                    self.line_index = len(self.text_lines)
                    self.char_index = 0
                    self.audio.stop_sound(setting.SoundEffect.TYPING_PATH)
                    self.animator.reset()

    def update(self):
        self.frame_count += 1

        if self.overlay_alpha < 200:
            self.overlay_alpha += 4
            
        if self.line_index < len(self.text_lines) and self.frame_count % self.type_speed == 0:
            # 重複播放音效
            if self.line_index == 0 and self.char_index == 0:
                self.audio.play_sound(setting.SoundEffect.TYPING_PATH)
            
            if self.audio.is_sound_playing(setting.SoundEffect.TYPING_PATH) is False:
                self.audio.play_sound(setting.SoundEffect.TYPING_PATH)
                
            current_line = self.text_lines[self.line_index]
            if self.char_index < len(current_line):
                self.reveal_lines[self.line_index] += current_line[self.char_index]
                self.char_index += 1
            else:
                self.line_index += 1
                self.char_index = 0
        
        self.animator.update()

        if self.line_index >= len(self.text_lines):
            self.animator.reset()
            self.audio.stop_sound(setting.SoundEffect.TYPING_PATH)

        

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        screen.blit(self.overlay_surface, (0, 0))

        y = 150
        for line in self.reveal_lines:
            rendered = self.font.render(line, True, (255, 255, 255))
            screen.blit(rendered, (100, y))
            y += 75

        if self.line_index >= len(self.text_lines):
            hint = self.font.render("按 Enter 返回", True, (200, 200, 200))
            screen.blit(hint, (self.SCREEN_WIDTH - 300, self.SCREEN_HEIGHT - 60))

        self.animator.draw(screen)
