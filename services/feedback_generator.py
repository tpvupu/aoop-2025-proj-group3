import os
from typing import Dict, Any

try:
    # OpenAI Python SDK (as used in test.py)
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None


def _summarize_actions(player, until_week: int) -> Dict[str, Any]:
    """Aggregate the player's choices up to a specific week.

    Returns a dict like:
    {"study": n, "rest": n, "socialize": n, "play_game": n, "total": n}
    """
    counts = {"study": 0, "rest": 0, "socialize": 0, "play_game": 0}
    # player.chosen is a 17-length list with action strings per week index
    for week_idx in range(1, min(until_week + 1, len(player.chosen))):
        act = player.chosen[week_idx]
        if act in counts:
            counts[act] += 1
    counts["total"] = sum(counts.values())
    return counts


def generate_weekly_advice(player, week: int) -> str:
    """Generate weekly advice using OpenAI API if available; fallback to heuristic text."""
    # Prefer OpenAI if SDK and key exist
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            counts = _summarize_actions(player, until_week=week)
            entry = player.event_history.get(week, {})
            event_text = entry.get("event_text", "")
            option_text = entry.get("option_text", "")
            choice_summary = option_text + " " + event_text 
            
            prompt = (
                f"你是玩家的學習顧問。根據以下資訊給予本週建議：\n\n"
                f"【玩家資料】\n"
                f"角色：{player.chname}（{player.name}）\n"
                f"第 {week} 週\n"
                f"目前屬性：心情 {player.mood}，體力 {player.energy}，社交 {player.social}，知識 {player.knowledge:.0f}\n"
                f"累計行為（至本週）：讀書 {counts['study']} 次、休息 {counts['rest']} 次、社交 {counts['socialize']} 次、玩遊戲 {counts['play_game']} 次\n\n"
                f"本週玩家選擇為：{choice_summary}\n\n"
                f"第一行分析玩家本週選擇的可能個性(用'{player.chname}你'代稱玩家)為何\n（20字以內）\n"
                f"第二行給玩家一點回覆，盡量有趣或有梗一點（主要參照本週劇情與玩家選擇,20字以內）\n"
            )
            
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一個專業的學習與心理顧問。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            advice_text = resp.choices[0].message.content or "(未取得建議內容)"
            # persist to player for Diary scene reuse
            try:
                if hasattr(player, "weekly_advice") and isinstance(player.weekly_advice, dict):
                    player.weekly_advice[week] = advice_text
            except Exception:
                pass
            return advice_text
        except Exception as e:  # graceful fallback
            fallback = _heuristic_advice(player, week, error=str(e))
            try:
                if hasattr(player, "weekly_advice") and isinstance(player.weekly_advice, dict):
                    player.weekly_advice[week] = fallback
            except Exception:
                pass
            return fallback
    # Fallback: no SDK or no key
    local = _heuristic_advice(player, week)
    try:
        if hasattr(player, "weekly_advice") and isinstance(player.weekly_advice, dict):
            player.weekly_advice[week] = local
    except Exception:
        pass
    return local

'''
def _heuristic_advice(player, week: int, error: str | None = None) -> str:
    """Simple local advice when API is unavailable."""
    counts = _summarize_actions(player, until_week=week)
    mood, energy, social, knowledge = player.mood, player.energy, player.social, player.knowledge

    # personality summary
    if counts["study"] >= max(counts["rest"], counts["socialize"], counts["play_game"]):
        persona = "你偏向目標導向且重視成果，遇到壓力時能以規劃回應。"
    elif counts["socialize"] > counts["study"]:
        persona = "你以人際互動獲得能量，團隊與討論能讓你保持動力。"
    elif counts["rest"] > counts["study"]:
        persona = "你重視自我照顧與節奏，懂得在恢復後再出發。"
    else:
        persona = "你喜歡保持彈性與探索，多元嘗試能刺激你的學習熱忱。"

    # learning style and advice
    style = []
    if knowledge < 35 and counts["study"] >= 3:
        style.append("視覺化學習：用心智圖整理週目標")
    if social >= 60:
        style.append("社交學習：找同伴互考或共讀")
    if energy < 50:
        style.append("番茄鐘搭配休息：25/5 分鐘循環")
    if mood < 50:
        style.append("情緒暖機：先寫下三件感謝的事")
    if not style:
        style.append("實作導向：先做題再回看筆記")

    # micro actions
    micro = []
    micro.append("列三個可完成的小目標")
    micro.append("每天固定30分鐘專注學習")
    micro.append("安排一次短社交或運動")

    parts = [
        f"人格小結：{persona}",
        f"學習風格與策略：\n- " + "\n- ".join(style),
        f"下週微行動：\n- " + "\n- ".join(micro),
    ]

    if error:
        parts.append(f"(提示：AI 服務不可用，改用在地建議；{error})")

    return "\n\n".join(parts)
'''

def generate_final_advice(player) -> str:
    """Generate end-of-game summary advice (uses OpenAI if available)."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    counts = _summarize_actions(player, until_week=min(player.week_number, 16))

    if OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            
            # 整理 event_history 中的重要事件
            event_summary = []
            love_events = []  # 專門收集愛情相關事件
            
            for week, entry in sorted(player.event_history.items()):
                event_text = entry.get("event_text", "")
                option_text = entry.get("option_text", "")
                
                # 識別第5週（遇見crush）和第11週（告白）的愛情事件
                if week == 5:
                    love_events.append(f"第5週【遇見命中注定】：{option_text}")
                elif week == 11:
                    love_events.append(f"第11週【告白時刻】：{option_text}")
                
                # 其他重要事件也記錄
                event_summary.append(f"第{week}週：{option_text}")
            
            event_summary_text = "\n".join(event_summary) if event_summary else "無特殊事件"
            love_summary_text = "\n".join(love_events) if love_events else "愛情線沒有觸發"
            
            prompt = (
                f"你是玩家的好友，請用輕鬆、幽默、朋友般的語氣（可以帶點調侃），根據玩家的整個學期表現，寫一篇完整的結局建議。不要使用表情符號\n\n"
                f"【玩家資料】\n"
                f"角色：{player.chname}（{player.name}）\n"
                f"最終成績：GPA {player.GPA:.2f}，期中 {player.midterm} 分，期末 {player.final} 分，總分 {player.total_score}\n"
                f"最終屬性：心情 {player.mood}，體力 {player.energy}，社交 {player.social}，知識 {player.knowledge:.0f}\n"
                f"累計行為：讀書 {counts['study']} 次、休息 {counts['rest']} 次、社交 {counts['socialize']} 次、玩遊戲 {counts['play_game']} 次\n\n"
                f"【整學期事件選擇】\n{event_summary_text}\n\n"
                f"【愛情線事件】\n{love_summary_text}\n\n"
                f"請輸出以下三個部分：\n\n"
                f"1.  人格分析（150-250字）\n"
                f"   - 用心理測驗的風格，幽默一點\n"
                f"   - 從整學期的選擇分析玩家的性格特質\n"
                f"   - 可以調侃\n"
                f"   - 可以用一些梗\n\n"
                f"2.  愛情分析（100-150字）\n"
                f"   - 根據第5週和第11週的愛情事件選擇分析玩家的戀愛觀\n"
                f"   - 加入你對玩家感情態度的猜測和評論\n"
                f"   - 語氣要像好友八卦一樣輕鬆有趣\n"
                f"   - 如果沒有愛情事件或選擇逃避，也要調侃一下\n\n"
                f"3.  學習建議（80-120字）\n"
                f"   - 根據玩家的行為模式給出實用建議\n"
                f"   - 給 2-3 個具體可行的小建議\n\n"
                f"記住：不要用「您」，用「你」；不要太專業術語，要像朋友聊天；可以用 emoji 但不要太多；語氣要活潑、真誠、有點搞笑。"
                f" 可以參考這些句子的語氣 : 你根本是卷王本王吧！整個學期狂讀書，是來學校修仙的嗎？、你是那種該衝的時候會衝、該躺的時候也不客氣的人。有點務實，但也懂得平衡，算是比較穩健的類型。、欸...你該不會以為大學就是來玩的吧？讀書次數少到我都替你捏把冷汗了。不過也許你就是那種臨時抱佛腳也能過的天才型？、社交小能手啊！你的人脈應該比我的存款還豐富吧。不過要小心別把太多時間花在聊天吃飯上，畢竟期末考不會因為你朋友多就放水。、有點邊緣人的感覺喔...不是說不好啦，但偶爾也該出來透透氣吧？宿舍不會長出新朋友的。、遊戲打這麼多，你是職業選手嗎？放鬆是好事，但別讓遊戲變成逃避現實的工具啊。、體力條已經見底了...你該不會每天熬夜吧？好好睡覺真的很重要，不是在開玩笑。、社交分數和社交次數雙低，你是隱士嗎？偶爾跟人聊聊天也不錯啦。"
               )     
        
            
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是玩家的好朋友，不是心理諮商師。用輕鬆幽默的方式給建議。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
            )
            return resp.choices[0].message.content or "(未取得建議內容)"
        except Exception as e:
            return _final_heuristic(player, counts, error=str(e))
    return _final_heuristic(player, counts)

'''
def _final_heuristic(player, counts: Dict[str, int], error: str | None = None) -> str:
    """Local end-of-game advice when API is unavailable."""
    mood, energy, social, knowledge = player.mood, player.energy, player.social, player.knowledge
    
    # 整理愛情事件
    love_week5 = player.event_history.get(5, {}).get("option_text", "")
    love_week11 = player.event_history.get(11, {}).get("option_text", "")
    
    # === 人格分析（像好友般的幽默分析）===
    persona_parts = []
    
    # 根據行為模式分析
    if counts["study"] >= 8:
        persona_parts.append("你根本是卷王本王吧！整個學期狂讀書，是來學校修仙的嗎？不過認真說，你這種目標導向的個性真的很適合需要長期投入的事情。")
    elif counts["study"] >= 5:
        persona_parts.append("你是那種該衝的時候會衝、該躺的時候也不客氣的人。有點務實，但也懂得平衡，算是比較穩健的類型。")
    elif counts["study"] <= 2:
        persona_parts.append("欸...你該不會以為大學就是來玩的吧？讀書次數少到我都替你捏把冷汗了。不過也許你就是那種臨時抱佛腳也能過的天才型？")
    
    if counts["socialize"] >= 6:
        persona_parts.append("社交小能手啊！你的人脈應該比我的存款還豐富吧。不過要小心別把太多時間花在聊天吃飯上，畢竟期末考不會因為你朋友多就放水。")
    elif counts["socialize"] <= 2:
        persona_parts.append("有點邊緣人的感覺喔...不是說不好啦，但偶爾也該出來透透氣吧？宿舍不會長出新朋友的。")
    
    if counts["play_game"] >= 6:
        persona_parts.append("遊戲打這麼多，你是職業選手嗎？放鬆是好事，但別讓遊戲變成逃避現實的工具啊。")
    
    if counts["rest"] >= 6:
        persona_parts.append("休息大師認證！你真的很懂得照顧自己，不過有時候該動的時候還是要動一下啦，不然會生鏽的。")
    
    # 根據最終屬性判斷
    if mood < 40:
        persona_parts.append("看你最後心情這麼低，這學期過得挺辛苦的吧？記得要找到讓自己開心的事情，不然會撐不下去的。")
    elif mood >= 80:
        persona_parts.append("你心情一直保持得不錯誒！這種正能量很珍貴，繼續保持這種態度吧。")
    
    if energy < 40:
        persona_parts.append("體力條已經見底了...你該不會每天熬夜吧？好好睡覺真的很重要，不是在開玩笑。")
    
    if social < 30 and counts["socialize"] < 3:
        persona_parts.append("社交分數和社交次數雙低，你是隱士嗎？偶爾跟人聊聊天也不錯啦。")
    
    persona = "🎭 人格分析\n\n" + " ".join(persona_parts)
    
    # === 愛情分析 ===
    love_analysis = "💕 愛情分析\n\n"
    
    if not love_week5 and not love_week11:
        love_analysis += "你這學期完全沒碰愛情線啊...是太專注學業還是根本沒遇到心動的對象？不過也沒關係啦，感情這種事強求不來。但如果你只是害羞，記得有時候要主動一點喔！"
    else:
        # 第5週分析
        if "主動出擊" in love_week5 or "要 IG" in love_week5:
            love_analysis += "第5週看到crush就直接要IG，你是行動派啊！這種積極的態度我喜歡，至少不會留遺憾。"
        elif "影響我拔刀" in love_week5 or "乖乖回宿舍" in love_week5:
            love_analysis += "遇到心動的對象居然選擇去讀書？你是理智型的，把學業看得比感情重。雖然很理性，但偶爾也可以放縱一下吧？"
        elif "手遊" in love_week5 or "度過一生" in love_week5:
            love_analysis += "寧願選手遊也不要戀愛...你是真愛遊戲啊！不過說真的，二次元老婆不會陪你吃飯啦。"
        elif "只在心裡" in love_week5 or "亂暈" in love_week5:
            love_analysis += "只敢暗戀不敢行動？你是慢熱型的，喜歡在心裡幻想但不敢踏出第一步。有時候勇敢一點也不錯喔！"
        
        # 第11週分析
        if "當然答應" in love_week11 or "脫單" in love_week11:
            love_analysis += " 而且第11週人家告白你就答應了，看來你也渴望被愛嘛！祝你們幸福啦哈哈。"
        elif "矜持" in love_week11 or "騙出洞" in love_week11:
            love_analysis += " 第11週居然拒絕告白？你是傲嬌嗎？還是真的不喜歡對方？小心錯過就沒了喔。"
        elif "海王" in love_week11 or "釣一下" in love_week11:
            love_analysis += " 第11週還在懷疑對方是海王，你也太小心了吧！信任也是感情的一部分啦。"
        elif "ㄍㄧㄥ不住" in love_week11 or "他也喜歡我" in love_week11:
            love_analysis += " 第11週超有自信的說「我就知道」，你是自戀型的嗎？不過有自信也不錯啦！"
    
    # === 學習建議 ===
    study_advice = "📚 學習建議\n\n"
    
    if player.GPA < 2.5:
        study_advice += "欸你的成績真的需要加油了！下學期記得：1) 每週至少認真讀書3-4次，2) 考前兩週開始複習不要拖，3) 找個讀書夥伴互相督促。"
    elif player.GPA < 3.5:
        study_advice += "成績還可以，但還有進步空間。建議你：1) 把讀書和娛樂時間分配得更明確一點，2) 考試前做一些考古題，3) 保持規律作息，累了就好好休息。"
    else:
        study_advice += "你成績很棒誒！繼續保持這個節奏就好。不過也別太拼，記得：1) 適度放鬆也是學習的一部分，2) 多跟朋友交流可以學到不同觀點，3) 保持好奇心繼續探索。"
    
    # 根據屬性給額外建議
    extra_tips = []
    if energy < 50:
        extra_tips.append("你體力太差了，多睡覺少熬夜！")
    if mood < 50:
        extra_tips.append("心情不好記得找人聊聊或做點開心的事")
    if social < 40:
        extra_tips.append("偶爾約朋友出去走走吧，別當獨行俠")
    
    if extra_tips:
        study_advice += " 還有：" + "、".join(extra_tips) + "。"
    
    # 組合結果
    result_parts = [persona, love_analysis, study_advice]
    
    if error:
        result_parts.append(f"\n(提示：AI建議功能暫時不可用，這是本地版建議。錯誤：{error})")
    
    return "\n\n".join(result_parts)

'''