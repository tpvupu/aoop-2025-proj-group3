import pygame
import os
import setting
from UI.components.audio_manager import AudioManager
import asyncio

class BaseScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 1200
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.audio = AudioManager.get_instance()
        

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def update(self):
        pass  # 由子類別實作

    def draw(self):
        pass  # 由子類別實作

    async def run(self):
        while self.running:
            await asyncio.sleep(0)  # Yield control for web compatibility
            result = None
            result = self.update()
            if result is not None:
                print(f"Scene result: {result}")
                return result
                
                
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return None 


    def load_frames(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.char_size)
                frames.append(img)
        return frames
    

    
def wrap_text(text, font, max_width):
    
    lines = []
    paragraphs = text.split('\n')  # 支援多段落

    for para in paragraphs:
        current_line = ""
        for char in para:
            test_line = current_line + char
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        if current_line:
            lines.append(current_line)

    return lines

def draw_wrapped_text(surface, text, font, rect, text_color=(0,0,0), line_height=None):
    lines = wrap_text(text, font, rect.width-20)
    if line_height is None:
        line_height = font.get_height()
    total_height = line_height * len(lines)
    start_y = rect.top + (rect.height - total_height) // 2

    for i, line in enumerate(lines):
        txt_surf = font.render(line, True, text_color)
        txt_rect = txt_surf.get_rect()
        txt_rect.left = rect.left + 20
        txt_rect.top = start_y + i * line_height
        surface.blit(txt_surf, txt_rect)

