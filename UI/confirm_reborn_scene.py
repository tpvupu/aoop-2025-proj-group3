
import pygame
import asyncio
from UI.components.base_scene import BaseScene
from UI.components.image_button import ImageButton
import setting
from UI.components.character_animator import CharacterAnimator


class ConfirmScene(BaseScene):
    def __init__(self, screen, blurred_bg, player):
        super().__init__(screen)
        self.blurred_bg = pygame.transform.scale(blurred_bg, screen.get_size())
        self.player = player
        self.message_font = pygame.font.Font(setting.CFONT_PATH, 32)
        self.message = "人生無法重來"
        self.message2 = "但可以重新投胎"
        self.message3 = "你確定要放棄我了嗎？"


        font = pygame.font.Font(setting.CFONT_PATH, 28)

        # 小確認框尺寸與位置
        self.box_width, self.box_height = 500, 700
        self.box_rect = pygame.Rect(
            (screen.get_width() - self.box_width) // 2,
            (screen.get_height() - self.box_height) // 2,
            self.box_width, self.box_height
        )

        # 載入小視窗圖片
        if self.player.name == "Bubu":
            window_img = setting.ImagePath.EVENT_BUBU_PATH
        elif self.player.name == "Yier":
            window_img = setting.ImagePath.EVENT_YIER_PATH
        elif self.player.name == "Mitao":
            window_img = setting.ImagePath.EVENT_MITAO_PATH
        elif self.player.name == "Huihui":
            window_img = setting.ImagePath.EVENT_HUIHUI_PATH

        self.window_img = pygame.image.load(window_img).convert_alpha()
        self.window_img = pygame.transform.smoothscale(self.window_img, (self.box_width, self.box_height))

        if self.player.name == "Yier" or self.player.name == "Huihui":
            self.animator = CharacterAnimator(self.player.sad , 
                                            (700,500),
                                            size=(200, 200))
            
        else:
            self.animator = CharacterAnimator(self.player.sad,
                                            (350,450),
                                            size=(200, 200))

        # 按鈕縮小並置於確認框下方
        btn_y = self.box_rect.bottom - 340
        self.button_yes = ImageButton(
            setting.ImagePath.YES_NO_IMG_PATH,
            (self.box_rect.left + 90, btn_y),
            size=(80, 40), text="是", font=font
        )
        self.button_no = ImageButton(
            setting.ImagePath.YES_NO_IMG_PATH,
            (self.box_rect.right - 150, btn_y),
            size=(80, 40), text="否", font=font
        )

    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            # 畫模糊背景
            self.screen.blit(self.blurred_bg, (0, 0))

            # 畫半透明遮罩
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.screen.blit(overlay, (0, 0))

            # 畫小視窗圖片
            self.screen.blit(self.window_img, self.box_rect.topleft)

            # 顯示訊息文字
            msg_surface = self.message_font.render(self.message, True, (80, 60, 50))
            msg_rect = msg_surface.get_rect(center=(self.box_rect.left + self.box_width // 2, self.box_rect.top + 180))
            self.screen.blit(msg_surface, msg_rect)
            msg_surface2 = self.message_font.render(self.message2, True, (80, 60, 50))
            msg_rect2 = msg_surface2.get_rect(center=(self.box_rect.left + self.box_width // 2, self.box_rect.top + 240))
            self.screen.blit(msg_surface2, msg_rect2)
            msg_surface3 = self.message_font.render(self.message3, True, (80, 60, 50))
            msg_rect3 = msg_surface3.get_rect(center=(self.box_rect.left + self.box_width // 2, self.box_rect.top + 300))
            self.screen.blit(msg_surface3, msg_rect3)

            # 更新 & 繪製按鈕
            self.button_yes.update()
            self.button_no.update()
            self.button_yes.draw(self.screen)
            self.button_no.draw(self.screen)

            # 畫角色動畫
            self.animator.update()
            self.animator.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_yes.is_clicked(event):
                        #print("[ConfirmScene] 收到 RESTART，return 中")
                        return "RESTART"
                    elif self.button_no.is_clicked(event):
                        return "BACK"

            pygame.display.flip()
            self.clock.tick(self.FPS)