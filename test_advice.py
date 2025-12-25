"""測試結局建議功能"""
from character import Huihui
from services.feedback_generator import generate_final_advice

# 創建測試角色
player = Huihui()
player.week_number = 16

# 模擬一些選擇和事件歷史
player.chosen = ['0', 'study', 'study', 'socialize', 'rest', 'study', 
                 'socialize', 'play_game', 'study', 'rest', 'study',
                 'socialize', 'play_game', 'rest', 'study', 'study', 'study']

# 模擬愛情事件
player.event_history = {
    5: {
        "event_text": "某天上課陽光灑進教室…你的眼神和對方交會的一瞬間時間彷彿凝結了三秒半。",
        "option_text": "主動出擊，跟他要 IG",
        "changes": {"mood": 5, "energy": -5, "social": 12, "knowledge": 2}
    },
    11: {
        "event_text": "你心儀的對象居然跟你告白了？！",
        "option_text": "什麼？！我這個萬年哥布林也有機會脫單嗎，當然答應",
        "changes": {"mood": 15, "energy": -5, "social": 15, "knowledge": 1}
    },
    3: {
        "event_text": "第一次小考",
        "option_text": "認真準備考試",
        "changes": {"mood": -5, "energy": -10, "social": 0, "knowledge": 15}
    }
}

# 模擬一些屬性
player.mood = 75
player.energy = 55
player.social = 70
player.knowledge = 65
player.midterm = 78
player.final = 82
player.GPA = 3.5
player.total_score = 80

print("=== 測試結局建議 ===\n")
print("角色資訊：")
print(f"- 姓名：{player.chname}")
print(f"- GPA：{player.GPA}")
print(f"- 期中/期末：{player.midterm}/{player.final}")
print(f"- 屬性：心情{player.mood} 體力{player.energy} 社交{player.social} 知識{player.knowledge}")
print(f"- 讀書次數：{player.chosen.count('study')}")
print(f"- 社交次數：{player.chosen.count('socialize')}")
print(f"- 愛情事件：第5週和第11週都有選擇")
print("\n" + "="*60 + "\n")

advice = generate_final_advice(player)
print(advice)
print("\n" + "="*60)
print("\n✅ 測試完成！建議內容已生成")
