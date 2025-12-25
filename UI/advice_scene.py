import pygame
from UI.components.base_scene import BaseScene, draw_wrapped_text, wrap_text
from UI.components.character_animator import CharacterAnimator
from UI.components.audio_manager import AudioManager
import setting


class AdviceScene(BaseScene):
    """心理測驗結果與學習建議專題場景"""

    def __init__(self, screen, player):
        super().__init__(screen)
        self.player = player
        self.audio = AudioManager.get_instance()
        
        # 背景
        self.background = pygame.image.load(
            setting.ImagePath.BACKGROUND_PATH
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )
        self.background.set_alpha(80)
        
        # 字體
        self.title_font = pygame.font.Font(setting.JFONT_PATH_BOLD, 52)
        self.section_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 28)
        # 內容字體放大以提高可讀性
        self.content_font = pygame.font.Font(setting.JFONT_PATH_Light, 28)
        
        # 角色動畫
        self.animator = CharacterAnimator(
            self.player.ending, (80, 350), (250, 250)
        )
        self.animator.frame_delay = 3
        
        # 建議文本
        self.advice_text = None
        self.is_loading = True
        # 可滾動文字表面與偏移
        # 行為式滾動：將文字分行，使用行索引控制顯示範圍
        self.lines = []
        self.line_height = 0
        self.start_line = 0  # 從哪一行開始顯示
        self.max_start_line = 0
        # 內容內邊距（內縮）
        self.content_padding = 20
        
        # 返回按鈕提示
        self.prompt_font = pygame.font.Font(setting.JFONT_PATH_REGULAR, 24)
        self.prompt_text = "(按 ESC 或 Enter 返回)"
        self.prompt_surface = self.prompt_font.render(
            self.prompt_text, True, (100, 100, 100)
        )
        
        # 顯示位置：左上(340,122)，右下(1154,692)
        # 寬度 = 1154 - 340 = 814， 高度 = 692 - 122 = 570
        self.content_rect = pygame.Rect(340, 122, 814, 570)
        
        # 生成建議
        
        # 延遲生成建議，避免初始化時阻塞
        if self.advice_text is None:
            self._generate_advice()
    
    def _generate_advice(self):
        """背景生成建議"""
        try:
            from services.feedback_generator import generate_final_advice
            self.advice_text = generate_final_advice(self.player)
            self.audio.play_sound(setting.SoundEffect.BLING_PATH)
        except Exception as e:
            self.advice_text = f"(產生建議失敗)\n\n{str(e)}"
            self.audio.play_sound(setting.SoundEffect.DONG_PATH)
        finally:
            self.is_loading = False
                # 準備分行資料供行滾動使用
            self._prepare_text_lines()

    def _prepare_text_lines(self):
        # 保存先前行滾動狀態；若先前已貼底，新的內容加入後仍保持貼底
        prev_max_start = getattr(self, 'max_start_line', 0)
        prev_start = getattr(self, 'start_line', 0)
        # 只有當先前有超出可視行（prev_max_start>0）且已捲到底時，才視為貼底
        prev_at_bottom = (prev_max_start > 0 and prev_start >= prev_max_start)

        if not self.advice_text:
            self.lines = []
            self.line_height = self.content_font.get_linesize()
            self.start_line = 0
            self.max_start_line = 0
            return

        inner_width = self.content_rect.width - 2 * self.content_padding
        # 先用 wrap_text 分成多行
        lines = wrap_text(self.advice_text, self.content_font, inner_width)
        self.lines = lines
        self.line_height = self.content_font.get_linesize()

        # 計算可視行數
        inner_height = self.content_rect.height - 2 * self.content_padding
        visible_lines = max(1, inner_height // self.line_height)
        total_lines = len(lines)
        new_max_start = max(0, total_lines - visible_lines)
        self.max_start_line = new_max_start

        # 根據內容量決定 start_line：若內容少於或等於可見行，則 start_line=0
        if total_lines <= visible_lines:
            # 內容不足一頁，顯示全部並貼底（在 draw 時會做貼底處理）
            self.start_line = 0
        else:
            if prev_at_bottom:
                # 如果之前在底，保持貼底
                self.start_line = new_max_start
            else:
                # 保留原來的 start 行，並夾住範圍
                self.start_line = max(0, min(prev_start, new_max_start))
    
    def update(self):
        """更新動畫與狀態"""
        self.animator.update()
    
    def draw(self):
        """繪製場景"""
        self.screen.fill((245, 240, 225))
        self.screen.blit(self.background, (0, 0))
        
        # 半透明黑色遮罩
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 30))
        self.screen.blit(overlay, (0, 0))
        
        # 標題
        title = self.title_font.render("結果分析", True, (50, 50, 70))
        # 把標題放在面板上方，與 panel 左邊對齊，並向上偏移 50px
        title_rect = title.get_rect(topleft=(self.content_rect.left, self.content_rect.top - 70))
        self.screen.blit(title, title_rect)
        
        # 角色動畫
        self.animator.draw(self.screen)
        
        # 建議內容面板
        panel_bg = pygame.Surface(
            (self.content_rect.width + 20, self.content_rect.height + 20),
            pygame.SRCALPHA
        )
        panel_bg.fill((255, 255, 255, 200))
        self.screen.blit(
            panel_bg,
            (self.content_rect.left - 10, self.content_rect.top - 10)
        )
        
        # 面板邊框
        border_rect = pygame.Rect(
            self.content_rect.left - 10,
            self.content_rect.top - 10,
            self.content_rect.width + 20,
            self.content_rect.height + 20
        )
        pygame.draw.rect(self.screen, (120, 120, 160), border_rect, 3)
        
        # 建議文本（使用可滾動的 text_surface）
        padding = self.content_padding
        inner_x = self.content_rect.left + padding
        inner_y = self.content_rect.top + padding
        inner_width = self.content_rect.width - 2 * padding
        inner_height = self.content_rect.height - 2 * padding

        if self.is_loading:
            loading_text = self.content_font.render("正在生成建議...", True, (100, 100, 100))
            self.screen.blit(
                loading_text,
                (self.content_rect.centerx - loading_text.get_width() // 2, self.content_rect.centery - 20)
            )
        else:
            # 使用行式滾動顯示：根據 self.start_line 決定顯示哪幾行
            lines = getattr(self, 'lines', [])
            lh = getattr(self, 'line_height', self.content_font.get_linesize())
            total_lines = len(lines)
            visible_lines = max(1, inner_height // lh)

            if total_lines == 0:
                pass
            else:
                # 若 total_lines <= visible_lines，將文字貼齊底部
                if total_lines <= visible_lines:
                    y_start = inner_y + (inner_height - total_lines * lh)
                    start = 0
                else:
                    # 否則依 self.start_line 顯示 visible_lines
                    start = max(0, min(self.start_line, max(0, total_lines - visible_lines)))
                    y_start = inner_y

                # 繪製可見行
                for i in range(visible_lines):
                    idx = start + i
                    if idx >= total_lines:
                        break
                    txt = lines[idx]
                    txt_surf = self.content_font.render(txt, True, (30, 30, 30))
                    self.screen.blit(txt_surf, (inner_x, y_start + i * lh))

                # 繪製基於行的捲軸（放在內側）
                scrollbar_height = inner_height
                bar_w = 8
                bar_x = self.content_rect.right - padding // 2 - bar_w
                bar_y = inner_y
                pygame.draw.rect(self.screen, (220, 220, 220), (bar_x, bar_y, bar_w, scrollbar_height))
                if total_lines > visible_lines:
                    thumb_h = max(20, int((visible_lines / total_lines) * scrollbar_height))
                    thumb_y = bar_y + int((start / (total_lines - visible_lines)) * (scrollbar_height - thumb_h))
                else:
                    thumb_h = scrollbar_height
                    thumb_y = bar_y
                pygame.draw.rect(self.screen, (140, 140, 160), (bar_x, thumb_y, bar_w, thumb_h))
        
        # 返回提示
        prompt_rect = self.prompt_surface.get_rect(
            bottomright=(self.SCREEN_WIDTH - 20, self.SCREEN_HEIGHT - 20)
        )
        self.screen.blit(self.prompt_surface, prompt_rect)
        
        pygame.display.flip()
    
    def run(self):
        """主循環"""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    self.audio.play_sound(setting.SoundEffect.MENU_HOVER_PATH)
                    print ("CLICK", pos)
                elif event.type == pygame.MOUSEWHEEL:
                    # 滾輪：event.y >0 表示向上。以行為單位滾動
                    lines_per_tick = 3
                    if getattr(self, 'lines', None):
                        total_lines = len(self.lines)
                        lh = getattr(self, 'line_height', self.content_font.get_linesize())
                        inner_height_local = self.content_rect.height - 2 * self.content_padding
                        visible_lines_local = max(1, inner_height_local // lh)
                        max_start = max(0, total_lines - visible_lines_local)
                        # 向上滾動會減少 start_line
                        self.start_line -= event.y * lines_per_tick
                        self.start_line = max(0, min(self.start_line, max_start))
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        self.audio.play_sound(setting.SoundEffect.DONG_PATH)
                        return "END"
            
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
