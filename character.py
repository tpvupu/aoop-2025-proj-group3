import random
import math
import setting
from UI.components.character_animator import CharacterAnimator
from event.gif_for_options import bubu, yier, mitao, huihui
import json
class Character:
    def __init__(self, name, intelligence, mood, energy, social):
        self.name = name
        self.intelligence = int(intelligence)
        self.mood = int(mood)
        self.energy = int(energy)
        self.social = int(social)
        self.knowledge = 0.00
        self.midterm = 0     # 期中考成績
        self.final = 0       # 期末考成績
        self.week_number = 0
        self.lucky_prof = 3
        self.total_score = 0
        self.GPA = 0
        self.chosen = ['0']*17
        self.home = ""
        self.last_week_change = [0,0,0,0]  # [心情, 體力, 社交, 知識]
        with open("event/events.json", "r", encoding="utf-8") as f:
            self.all_weeks_data = json.load(f)
        self.week_data = None
        self.event_history = {}  # key: week_number, value: {event_text, option_text, changes}


    def study(self, degree):
        growth = int(
            self.intelligence * 0.11 +
            self.mood * 0.05 +
            self.energy * 0.08 +
            self.social * 0.03
        )
        growth = round(growth/(1+((8 - self.week_number) * 0.1)),2) if self.week_number < 8 else round(growth/(1+((16 - self.week_number) * 0.1)),2)
        self.last_week_change = [-int(growth*0.8), -int(growth*0.5)-3, 0, growth+1]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change] 
        
        self.mood , self.energy , self.social, self.knowledge = \
            max(0, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            max(0, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3]) 

    def socialize(self, degree):
        growth = int(
            (self.social - 30) * 0.1 +
            (self.mood - 50) * 0.03 +
            (self.energy) * 0.01
        )
        self.last_week_change = [ 4, -5, growth, 4+int(round(growth * self.social * 0.01))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change] 
        
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            min(100, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3]) 

        #print(f"{self.name} 正在社交中 🤝🎉 社交能力提升了 {growth:.2f} 點！現在是 {self.social}/100")

    def play_game(self, degree):
        growth = int(
            (100 - self.mood) * 0.2 +
            (self.intelligence - 30) * 0.02 +
            (self.energy) * 0.01 -
            (self.social) * 0.01
        )
        self.last_week_change = [growth, int(growth*0.2), 1, 1+int(round(-growth * 0.1))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change] 
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            min(100, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3])
        #print(f"{self.name} 正在玩遊戲 🎮😄 心情提升了 {growth:.2f} 點！現在是 {self.mood}/100")

    def rest(self, degree):
        growth = int(
            (100 - self.energy) * 0.15 +
            (100 - self.mood) * 0.02 +
            (self.intelligence - 50) * 0.2 -
            (self.social - 30) * 0.01
        )
        self.last_week_change = [int(growth*0.6), growth, 1, 2+int(round(-growth * 0.1))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change]
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            min(100, self.energy + self.last_week_change[1]),\
            min(100,max(0, self.social + self.last_week_change[2])),\
            min(100, self.knowledge + self.last_week_change[3])
        #print(f"{self.name} 正在休息 💤😌 體力提升了 {growth:.2f} 點！現在是 {self.energy}/100")

    def calculate_grade(self):
        score = round(self.knowledge * 0.45 + self.mood * 0.3 + self.energy * 0.2 + self.intelligence * 0.1 , 2)
        #成績的粗略計算，後續有進行調分
        if score >= 60:
            return random.randint(int(score - 1), int(score + 15))
        else:
            luck = random.random()
            base = round(score * 0.85, 2)
            fluctuation_range = round(5 + luck * 20, 2)
            fluctuation = round(random.uniform(luck, fluctuation_range), 2)
            grade = min(100, round(base + fluctuation, 2))
        return int(round(grade))
    
    def get_final(self):
        self.final = round(self.calculate_grade()) -15

    def calculate_GPA(self):
        total_score = self.midterm * 0.35 + self.final * 0.35 + (self.knowledge) * 0.3
        total_score = max(0, int(math.sqrt(total_score) * 13 - 30))#適當調分
        self.total_score = total_score
        gpa = []
        for _ in range(25):
            if random.random() < 0.8:
                gpa.append(min(4.3,score_to_gpa(total_score) + self.lucky_prof * 0.03))
            else:
                gpa.append(score_to_gpa(total_score))
        self.GPA = round(sum(gpa) / len(gpa),2)
        #print(f"total_score: {total_score}, GPA: {self.GPA:.2f}, lucky_prof: {self.lucky_prof}")
        #print(gpa)

    def show_status(self):
        pass
        #print(f"{self.name} 在第{self.week_number - 1}週的狀態：")
        #print(f"智力：{self.intelligence} | 心情：{self.mood} | 體力：{self.energy} | 社交：{self.social} | 知識：{self.knowledge:.2f}/100")
        #print("===========================================================")


# 🧸 各角色子類別
class Bubu(Character):
    def __init__(self):
        super().__init__("Bubu", intelligence=70, mood=75, energy=90, social=30)
        self.chname = "布布"
        self.animal = "熊熊"
        self.header = setting.ImagePath.BUBU_HEAD_PATH
        self.intro = setting.GIF_PATHS['BUBU_INTRO_FRAMES']
        self.storytyping = setting.GIF_PATHS['BUBU_PLAYCOMPUTER_FRAMES']
        self.testing = setting.GIF_PATHS['BUBU_STUDY_FRAMES']
        self.taketest = setting.GIF_PATHS['BUBU_NO_STUDY_FRAMES']       
        self.ending = setting.GIF_PATHS['BUBU_HAPPY_FRAMES']
        self.sad = setting.GIF_PATHS['BUBU_CRYING_FRAMES']

        
        self.low_mood_limit = 30
        self.low_energy_limit = 30
        self.low_social_limit = 30
        self.low_knowledge_limit = 30
        self.high_mood_limit = 80
        self.high_energy_limit = 80
        self.high_social_limit = 80
        self.high_knowledge_limit = 80
        
        
    def gif_choose(self, weeknum , pos = (400, 400), size = (300, 300)):
        self.animator = CharacterAnimator(self.intro, pos, size)
        if weeknum == 0:
            return self.animator    
        
        #根據選擇撥放不同的動畫
        option = self.chosen[weeknum]
        if option in bubu[f"week_{weeknum}"]:
            self.animator = CharacterAnimator(bubu[f"week_{weeknum}"][option], pos, size)
            
        return self.animator

    def socialize(self, degree):
        growth = round(
            (100 - self.social) * 0.1 +
            (self.mood - 30) * 0.03 +
            (self.energy) * 0.01, 2
        )

        self.last_week_change = [ 3, -15, growth, 3+int(round(growth * self.social * 0.01))]
        self.last_week_change = [int(grow * degree) for grow in self.last_week_change]
        self.mood , self.energy , self.social, self.knowledge = \
            min(100, self.mood + self.last_week_change[0]),\
            max(0, self.energy + self.last_week_change[1]),\
            max(0, self.social + self.last_week_change[2]),\
            min(100, self.knowledge + self.last_week_change[3])
        
    def get_midterm(self):
        self.midterm = self.calculate_grade() + self.knowledge * 0.4
        if self.mood > 65:
            self.midterm += 6
        if self.energy < 70:
            self.midterm -= 2
        if self.knowledge > 35:
            self.midterm += 6
        self.midterm = int(round(self.midterm))


class Yier(Character):
    def __init__(self):
        super().__init__("Yier", intelligence=75, mood=85, energy=60, social=90)
        self.animal = "熊熊"
        self.chname = "一二"
        self.header = setting.ImagePath.YIER_HEAD_PATH
        
        self.intro = setting.GIF_PATHS['YIER_INTRO_FRAMES']
        self.storytyping = setting.GIF_PATHS['YIER_PLAY_GAME_FRAMES']
        self.testing = setting.GIF_PATHS['YIER_THINKING_FRAMES']
        self.taketest = setting.GIF_PATHS['YIER_NO_STUDY_FRAMES']
        self.ending = setting.GIF_PATHS['YIER_EXCITING_FRAMES']
        self.sad = setting.GIF_PATHS['YIER_SAD_FRAMES']
    

        self.low_mood_limit = 30
        self.low_energy_limit = 30
        self.low_social_limit = 30
        self.low_knowledge_limit = 30
        self.high_mood_limit = 80
        self.high_energy_limit = 80
        self.high_social_limit = 80
        self.high_knowledge_limit = 80
        
        
    def gif_choose(self, weeknum , pos = (400, 400), size = (300, 300)):
        self.animator = CharacterAnimator(self.intro, pos, size)
        if weeknum == 0:
            return self.animator    
        
        #根據選擇撥放不同的動畫
        option = self.chosen[weeknum]
        if option in yier[f"week_{weeknum}"]:
            self.animator = CharacterAnimator(yier[f"week_{weeknum}"][option], pos, size)
            
        return self.animator
   

    def get_midterm(self):
        self.midterm = min(100, self.calculate_grade() + self.knowledge * 0.2)
        if self.social > 80:
            self.midterm += 2
        if self.energy < 50:
            self.midterm -= 3
        if self.knowledge > 40:
            self.midterm += 4
        self.midterm = int(round(self.midterm))


class Mitao(Character):
    def __init__(self):
        super().__init__("Mitao", intelligence=95, mood=50, energy=45, social=60)
        self.animal = "貓貓"
        self.chname = "蜜桃"
        self.header =  setting.ImagePath.MITAO_HEAD_PATH

        self.intro = setting.GIF_PATHS['MITAO_CHIP_FRAMES']
        self.storytyping = setting.GIF_PATHS['MITAO_REST_FRAMES']
        self.testing = setting.GIF_PATHS['MITAO_TESTING_FRAMES']
        self.taketest = setting.GIF_PATHS['MITAO_LOW_MOOD_FRAMES']
        self.ending = setting.GIF_PATHS['MITAO_FLOWER_FRAMES']
        self.sad = setting.GIF_PATHS['MITAO_LOW_MOOD_FRAMES']
        
        
        self.low_mood_limit = 30
        self.low_energy_limit = 30
        self.low_social_limit = 30
        self.low_knowledge_limit = 30
        self.high_mood_limit = 80
        self.high_energy_limit = 80
        self.high_social_limit = 80
        self.high_knowledge_limit = 80
        
    def gif_choose(self, weeknum , pos = (400, 400), size = (300, 300)):
        self.animator = CharacterAnimator(self.intro, pos, size)
        if weeknum == 0:
            return self.animator    
        
        #根據選擇撥放不同的動畫
        option = self.chosen[weeknum]
        if option in mitao[f"week_{weeknum}"]:
            self.animator = CharacterAnimator(mitao[f"week_{weeknum}"][option], pos, size)
            
        return self.animator

        


    def get_midterm(self):
        self.midterm = min(100, self.calculate_grade() + self.knowledge * 0.2)
        self.midterm += 6
        if self.mood < 60:
            self.midterm -= 4
        if self.knowledge > 45:
            self.midterm += 5
        self.midterm = int(round(self.midterm))



class Huihui(Character):
    def __init__(self):
        super().__init__("Huihui", intelligence=80, mood=90, energy=50, social=65)
        self.animal = "貓貓"
        self.chname = "灰灰"
        
        self.header = setting.ImagePath.HUIHUI_HEAD_PATH
        self.intro = setting.GIF_PATHS['HUIHUI_INTRO_FRAMES']
        self.storytyping = setting.GIF_PATHS['HUIHUI_REST_FRAMES']  
        self.taketest = setting.GIF_PATHS['HUIHUI_SOSAD_FRAMES']
        self.testing = setting.GIF_PATHS['HUIHUI_RUNNING_FRAMES']
        self.ending = setting.GIF_PATHS['HUIHUI_FLOWER_FRAMES']
        self.sad = setting.GIF_PATHS['HUIHUI_SAD_FRAMES']
        self.week_number = 0
        
         
        self.low_mood_limit = 30
        self.low_energy_limit = 30
        self.low_social_limit = 30
        self.low_knowledge_limit = 30
        self.high_mood_limit = 80
        self.high_energy_limit = 80
        self.high_social_limit = 80
        self.high_knowledge_limit = 80
        
        
    
    def gif_choose(self, weeknum , pos = (400, 400), size = (300, 300)):
        self.animator = CharacterAnimator(self.intro, pos, size)
        if weeknum == 0:
            return self.animator    
        
        #根據選擇撥放不同的動畫
        option = self.chosen[weeknum]
        if option in huihui[f"week_{weeknum}"]:
            self.animator = CharacterAnimator(huihui[f"week_{weeknum}"][option], pos, size)
            
        return self.animator

        

    def get_midterm(self):
        self.midterm = min(100, self.calculate_grade() + self.knowledge * 0.2)
        if self.mood > 85:
            self.midterm += 5
        if self.energy < 50:
            self.midterm -= 3
        if self.knowledge > 30:
            self.midterm += 2
        self.midterm = int(round(self.midterm))



def score_to_gpa(score):
    if score >= 95:
        return 4.3
    grading = 95/4.3 # 95分對應4.3
    return round(score / grading, 2) 
    


if __name__ == "__main__":
    player = Huihui()

    player.socialize(1)
    player.socialize(1)
    player.rest(1)
    player.play_game(1)
    player.study(1)
    player.socialize(1)
    player.rest(1)
    player.study(1)

    player.get_midterm()

    player.study(1)
    player.socialize(1)
    player.rest(1)
    player.study(1)
    player.study(1)
    player.rest(1)
    player.study(1)
    player.study(1)

    player.get_final()

    player.calculate_GPA()

    print(f"{player.name} 的期中考成績：{player.midterm}")
    print(f"{player.name} 的期末考成績：{player.final}")
    
    print(f"{player.name} 的知識：{player.knowledge}")
    print(f"{player.name} 的 GPA: {player.GPA}")
    print(f"{player.name} 的社交能力：{player.social}")
    print(f"{player.name} 的幸運教授：{player.lucky_prof}")
    print(f"{player.name} 的心情：{player.mood}")
    print(f"{player.name} 的體力：{player.energy}")
    # player.show_status()