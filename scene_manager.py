import pygame
from UI.character_select import CharacterSelectScene
from UI.start_scene import StartScene
from UI.intro_scene import IntroScene
from UI.story_scene import StoryScene
from UI.event_scene import EventScene
from UI.set_scene import SetScene
from character import Bubu, Yier, Mitao, Huihui
from UI.components.first_scene import FirstScene
from UI.main_scene import MainScene
from UI.rank_scene import RankScene
from UI.diary_scene import DiaryScene
from UI.sound_control_scene import SoundControlScene
from UI.end_scene import EndScene
from UI.feedback_scene import FeedbackScene
from UI.advice_scene import AdviceScene
import asyncio

# scene_manager.py
class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.player = None
        self.scene_map = {
            "FIRST": self.first_scene,
            "START": self.start_scene,
            "CHARACTER_SELECT": self.character_select,
            "MAIN": self.main_game_loop,
            "STORY": self.story_and_event,
            "SETTING": self.setting_scene,
            "SOUND_CONTROL":  self.sound_control_scene,
            "SHOW_INTRO": self.intro_scene,
            "RANK": self.rank_scene,
            "END": self.end_scene,
            "ADVICE": self.advice_scene,
            "FEEDBACK": self.feedback_scene,
            "RESTART": self.restart_game,
            "QUIT": self.quit_game,
            "DIARY": self.diary_scene
        }

    async def run(self):
        # print("SceneManager 開始跑了")
        next_scene = "FIRST"
        while self.running and next_scene:
            await asyncio.sleep(0)  # Yield control for web compatibility
            # print(f"[SceneManager] 下一個場景是：{next_scene}") 
            handler = self.scene_map.get(next_scene)
            if handler:
                next_scene = await handler()
            else:
                print(f"未知場景：{next_scene}")
                self.running = False

    # --- 各個場景 ---
    async def first_scene(self):
        scene = FirstScene(self.screen)
        result = await scene.run()
        return {
            "START": "START",
            "QUIT": "QUIT"
        }.get(result, "FIRST")

    async def start_scene(self):
        # print("[SceneManager] 進入 start_scene")
        scene = StartScene(self.screen)
        result = await scene.run()
        # print(f"[SceneManager] StartScene 回傳：{result}") 
        return {
            "START": "CHARACTER_SELECT",
            "SHOW_INTRO": "SHOW_INTRO",
            "SOUND_CONTROL": "SOUND_CONTROL",
            "QUIT": "QUIT"
        }.get(result, "START")
    
    async def intro_scene(self):
        scene = IntroScene(self.screen)
        await scene.run()
        return "START"

    async def character_select(self):
        scene = CharacterSelectScene(self.screen)
        selected = await scene.run()
        if selected == "布布 Bubu":
            self.player = Bubu()
        elif selected == "一二 Yier":
            self.player = Yier()
        elif selected == "蜜桃 Mitao":
            self.player = Mitao()
        elif selected == "灰灰 Huihui":
            self.player = Huihui()
        else:
            return "QUIT"
        return "MAIN"
    
    async def sound_control_scene(self):
        await SoundControlScene(self.screen).run()
        return "START" if self.player is None else "SETTING"

    async def main_game_loop(self):
        if self.player.week_number >= 16:
            return "END"

        scene = MainScene(self.screen, self.player)
        result = await scene.run()

        return {
            "Next Story": "STORY",
            "SETTING": "SETTING",
            "Quit": "QUIT",
            "DIARY": "DIARY",
            "RESTART": "CHARACTER_SELECT",
        }.get(result, "MAIN")

    async def story_and_event(self):
        self.player.week_number += 1
        self.player.week_data = self.player.all_weeks_data[f"week_{self.player.week_number}"]
        await StoryScene(self.screen, self.player).run()
        await EventScene(self.screen, self.player).run()
        return "MAIN"

    async def setting_scene(self):
        from UI.components.blur import fast_blur
        blurred = fast_blur(self.screen.copy())
        set_scene = SetScene(self.screen, blurred, self.player)
        result = await set_scene.run()
        # print(f"[SceneManager] SetScene 回傳：{result}") 
        return {
            "BACK": "MAIN",
            "RESTART": "CHARACTER_SELECT",
            "SOUND_CONTROL": "SOUND_CONTROL",
            "QUIT": "QUIT"
        }.get(result, "MAIN")

    
    async def diary_scene(self):
        # print("進入日記場景")
        scene = DiaryScene(self.screen, self.player)
        result = await scene.run()
        #return "MAIN" if result == "BACK" else result
        if  self.player.week_number < 16:
            return {
                "BACK": "MAIN",
                "QUIT": "QUIT"
            }.get(result, "MAIN")
        else:
            return {
                "BACK": "END",
                "QUIT": "QUIT"
            }.get(result, "END")

    async def end_scene(self):
        if not self.player.GPA:
            self.player.calculate_GPA()

        scene = EndScene(self.screen, self.player)
        result = await scene.run()
        return {
            "DIARY": "DIARY",
            "SHOW_RANK": "RANK",
            "ADVICE": "ADVICE",
            "RESTART": "RESTART",
            "FEEDBACK": "FEEDBACK",
            "QUIT": "QUIT"
        }.get(result, "END")

    async def advice_scene(self):
        scene = AdviceScene(self.screen, self.player)
        result = await scene.run()
        return {
            "END": "END",
            "QUIT": "QUIT"
        }.get(result, "END")


    async def rank_scene(self):
        scene = RankScene(self.screen, self.player)
        await scene.run()
        return "END"
    
    async def feedback_scene(self):
        await FeedbackScene(self.screen, self.player).run()
        return "END"

    async def restart_game(self):
        # print("[SceneManager] restart_game 觸發了！")
        self.player = None
        return "START"

    async def quit_game(self):
        self.running = False
        return  "QUIT"
