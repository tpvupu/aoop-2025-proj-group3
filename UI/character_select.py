import pygame
from UI.components.base_scene import BaseScene
from UI.components.audio_manager import AudioManager
import setting
import asyncio


class CharacterSelectScene(BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        # ---------------- 基本參數 ----------------
        self.frame_index = 0
        self.hovered_character = None
        self.char_size = (140, 140)
        self.box_width, self.box_height = 500, 300
        self.margin = 30
        self.selected_character = None

        
        self.font = pygame.font.Font(setting.JFONT_PATH_BOLD, 36)
        self.font_desc = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)


        # ---------------- 音樂 ----------------
        self.audio = AudioManager.get_instance()
        self.audio.play_bgm(setting.BGM.MITAO_HUIHUI_PATH)
        


        # ---------------- 背景 ----------------
        self.background = pygame.image.load(
            setting.ImagePath.BACKGROUND_PATH
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )
        self.background.set_alpha(100)

         

        # ---------------- 角色資料 ----------------
        self.characters = [
            {
                "name": "布布 Bubu",
                "frames": self.load_frames(setting.GIF_PATHS["BUBU_INTRO_FRAMES"]),
                "description": (
                    "大家好～我是布布！\n我喜歡在網路上盡情地打遊戲！ \n"
                    "希望這學期所有的課都可以過 \n教授...菜菜...撈撈..."
                ),
                "box": pygame.Rect(
                    self.margin, self.margin, self.box_width, self.box_height
                ),
                "color": (255, 200, 200),
                "hover_color": (200, 100, 100),
            },
            {
                "name": "一二 Yier",
                "frames": self.load_frames(setting.GIF_PATHS["YIER_INTRO_FRAMES"]),
                "description": (
                    "大家好～我是一二！\n我熱衷於系上活動以及社團～ \n"
                    "認識好多學長姐嘿嘿～ \n到處吃瓜聽八卦真爽！"
                ),
                "box": pygame.Rect(
                    self.SCREEN_WIDTH - self.margin - self.box_width,
                    self.margin,
                    self.box_width,
                    self.box_height,
                ),
                "color": (150, 200, 255),
                "hover_color": (100, 150, 200),
            },
            {
                "name": "蜜桃 Mitao",
                "frames": self.load_frames(setting.GIF_PATHS["MITAO_INTRO_FRAMES"]),
                "description": (
                    "大家好～我是蜜桃！\n嗚嗚嗚這學期不小心選太多課... \n"
                    "現在實在是捲不動了～ \n但我還是會努力拿卷的！"
                ),
                "box": pygame.Rect(
                    self.margin,
                    self.SCREEN_HEIGHT - self.margin - self.box_height,
                    self.box_width,
                    self.box_height,
                ),
                "color": (255, 200, 200),
                "hover_color": (255, 120, 180),
            },
            {
                "name": "灰灰 Huihui",
                "frames": self.load_frames(setting.GIF_PATHS["HUIHUI_INTRO_FRAMES"]),
                "description": (
                    "大家好～我是灰灰！\n我正在追求自己真正想做的事!\n"
                    "讀書不是重點 ! \n重要的是追尋我的快樂貓生！"
                ),
                "box": pygame.Rect(
                    self.SCREEN_WIDTH - self.margin - self.box_width,
                    self.SCREEN_HEIGHT - self.margin - self.box_height,
                    self.box_width,
                    self.box_height,
                ),
                "color": (200, 200, 200),
                "hover_color": (80, 80, 80),
            },
        ]

    # ------------------------------------------------------------------
    # 更新：事件處理、動畫計時、hover 狀態與音效
    # ------------------------------------------------------------------
    def update(self):
        self.clock.tick(self.FPS)
        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        # ------- 事件 -------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for char in self.characters:
                    if char["box"].collidepoint(mouse_pos):
                        self.selected_character = char["name"]
                        return self.selected_character  # 回傳後 SceneManager 可切換場景

        # ------- 動畫更新 -------
        if pygame.time.get_ticks() % (1000 // self.FPS * 5) < (1000 // self.FPS):
            self.frame_index = (self.frame_index + 1) % len(self.characters[0]["frames"])

        # ------- hover 更新與音效 -------
        new_hover = None
        for char in self.characters:
            is_hovered = char["box"].collidepoint(mouse_pos)
            if is_hovered:
                new_hover = char["name"]
                if self.hovered_character != new_hover:
                    self.audio.play_sound(setting.SoundEffect.MENU_HOVER_PATH)
            # 可在此記錄 hover 旗標給 draw 使用（若需要動畫縮放等效果）
            char["is_hovered"] = is_hovered
        self.hovered_character = new_hover

        return None  # 無場景切換時回傳 None

    # ------------------------------------------------------------------
    # 繪製所有內容
    # ------------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for char in self.characters:
            rect = char["box"]
            is_hovered = char.get("is_hovered", False)

            # 角色框背景（帶透明度）
            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 220))
            self.screen.blit(overlay, rect.topleft)

            # 邊框
            border_color = char["hover_color"] if is_hovered else char["color"]
            pygame.draw.rect(self.screen, border_color, rect, 5)

            # 角色圖片（右下角對齊）
            frame = char["frames"][self.frame_index]
            img_x = rect.right - frame.get_width() - 20
            img_y = rect.bottom - frame.get_height() - 20
            self.screen.blit(frame, (img_x, img_y))

            # 名字（左下角）
            name_surface = self.font.render(char["name"], True, (50, 50, 50))
            self.screen.blit(name_surface, (rect.left + 20, rect.bottom - 50))

            # 描述（左上角，自動換行）
            desc_lines = [line for line in char["description"].split('\n') if line]
            for i, line in enumerate(desc_lines):
                line_surface = self.font_desc.render(line, True, (100, 100, 100))
                self.screen.blit(line_surface, (rect.left + 20, rect.top + 20 + i * 40))

        pygame.display.flip()

    # ------------------------------------------------------------------
    # 主循環：update → draw
    # ------------------------------------------------------------------
    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            result = self.update()
            if result is not None:   # 取得角色名稱或 "QUIT"
                return result
            self.draw()
