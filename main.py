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