import pygame
import os

class CharacterAnimator:
    
    def __init__(self, folder_path, position, size):
        self.folder_path = folder_path
        self.position = position  # (x, y)
        self.size = size          # (width, height)
        self.frames = []

        for filename in sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0])):
            if filename.endswith(".png"):
                #print('Loading frame:', filename)  # Debugging line to see which frames are loaded
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                self.frames.append(img)

        self.current_frame = 0
        self.frame_count = len(self.frames)
        self.frame_delay = 5  # 每幾幀換一張圖
        self.frame_timer = 0

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #print("滑鼠位置：", mouse_pos)

        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count

    def draw(self, screen):
        if self.frames:
            screen.blit(self.frames[self.current_frame], self.position)

    def get_rect(self):
        return pygame.Rect(self.position, self.size)


    def reset(self):
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_count = len(self.frames)

    def switch_animation(self, new_folder_path):
        self.folder_path = new_folder_path
        self.frames = []
        for filename in sorted(os.listdir(new_folder_path), key=lambda x: int(x.split('_')[1].split('.')[0])):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(new_folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                self.frames.append(img)

        self.current_frame = 0
        self.frame_count = len(self.frames)
        self.frame_timer = 0
        self.position = (self.position[0], self.position[1])