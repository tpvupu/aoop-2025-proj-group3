import pygame
from scene_manager import SceneManager
import setting
import asyncio

async def main():
    await asyncio.sleep(0)
    pygame.display.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))
    pygame.display.set_caption("Lazy Me Today Too")
    # 預防黑屏：顯示簡單載入畫面
    try:
        screen.fill((20, 20, 24))
        font = pygame.font.SysFont(None, 36)
        text = font.render("Loading... 點一下開始", True, (230, 230, 230))
        rect = text.get_rect(center=(setting.SCREEN_WIDTH//2, setting.SCREEN_HEIGHT//2))
        screen.blit(text, rect)
        pygame.display.flip()
    except Exception as _:
        pass
    
    manager = SceneManager(screen)
    if await manager.run() == "QUIT":
        pygame.quit()
        


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
        # In a web context, you might want to display this on the page itself.
        # For now, printing to the console is fine for debugging.