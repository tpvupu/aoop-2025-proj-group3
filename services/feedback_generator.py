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


def _build_prompt(player, week: int) -> str:
    """Build a structured Chinese prompt for weekly advice generation."""
    action_counts = _summarize_actions(player, until_week=week)
    entry = player.event_history.get(week, {})
    event_text = entry.get("event_text", "")
    option_text = entry.get("option_text", "")
    changes = entry.get("changes", {})

    changes_str = ", ".join([f"{k}:{v}" for k, v in changes.items()]) if changes else "(無)"

    prompt = (
        f"你是一位遊戲內的學習與心理顧問。\n"
        f"請根據玩家於第 {week} 週的選擇與狀態，輸出以下三段中文建議：\n"
        f"1) 心理測驗式的人格小結（以温柔、具體、正向的語氣，30~60字）\n"
        f"2) 學習風格判斷（如：視覺/聽覺/動手實作/社交學習），並給出2~3條可落地的策略建議\n"
        f"3) 下週可執行的微行動建議（3條、每條不超過20字）\n\n"
        f"【玩家基本資料】\n"
        f"角色：{player.chname}（{player.name}）\n"
        f"本週事件：{event_text}\n"
        f"本週選項：{option_text}\n"
        f"屬性變化：{changes_str}\n"
        f"當前屬性：心情:{player.mood} 體力:{player.energy} 社交:{player.social} 知識:{player.knowledge:.2f}\n"
        f"累計行為：讀書:{action_counts['study']} 休息:{action_counts['rest']} 社交:{action_counts['socialize']} 玩遊戲:{action_counts['play_game']}\n\n"
        f"請以簡潔條列輸出，不要加入JSON或程式碼，直接輸出人類可讀的中文。"
    )
    return prompt

'''
def generate_weekly_advice(player, week: int) -> str:
    """Generate weekly advice using OpenAI API if available; fallback to heuristic text."""
    # Prefer OpenAI if SDK and key exist
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            prompt = _build_prompt(player, week)
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "你是一個專業的學習與心理顧問。"},
                    {"role": "user", "content": prompt},
                ],
            )
            return resp.choices[0].message.content or "(未取得建議內容)"
        except Exception as e:  # graceful fallback
            return _heuristic_advice(player, week, error=str(e))
    # Fallback: no SDK or no key
    return _heuristic_advice(player, week)

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


def generate_final_advice(player) -> str:
    """Generate end-of-game summary advice (uses OpenAI if available)."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    counts = _summarize_actions(player, until_week=min(player.week_number, 16))

    if OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            prompt = (
                f"你是遊戲的結局顧問，請用中文輸出三段內容：\n"
                f"1) 心理測驗式人格總結（50~80字，正向中立）\n"
                f"2) 學習風格與最佳策略（3點）\n"
                f"3) 未來兩週的微行動（3條，每條≤20字）\n\n"
                f"【角色與結果】\n角色：{player.chname}（{player.name}）\n"
                f"GPA：{player.GPA:.2f}，期中：{player.midterm}，期末：{player.final}，總分：{player.total_score}\n"
                f"屬性：心情:{player.mood} 體力:{player.energy} 社交:{player.social} 知識:{player.knowledge:.0f}\n"
                f"累計行為：讀書:{counts['study']} 休息:{counts['rest']} 社交:{counts['socialize']} 玩遊戲:{counts['play_game']}\n\n"
                f"請用條列與段落，避免JSON或程式碼，語氣溫暖且務實。"
            )
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "你是一位專業的學習與心理顧問。"},
                    {"role": "user", "content": prompt},
                ],
            )
            return resp.choices[0].message.content or "(未取得建議內容)"
        except Exception as e:
            return _final_heuristic(player, counts, error=str(e))
    return _final_heuristic(player, counts)


def _final_heuristic(player, counts: Dict[str, int], error: str | None = None) -> str:
    """Local end-of-game advice when API is unavailable."""
    mood, energy, social, knowledge = player.mood, player.energy, player.social, player.knowledge
    # persona
    if player.GPA >= 3.8:
        persona = "你具備高穩定度與自我要求，能持續朝目標前進。"
    elif player.GPA >= 3.2:
        persona = "你兼顧彈性與紀律，懂得在現實與理想間調整步伐。"
    else:
        persona = "你重視體驗與探索，需要建立簡潔且可持續的習慣。"

    # style
    style = []
    if counts["study"] >= 6:
        style.append("視覺筆記：章節樹＋關鍵字卡片")
    if social >= 70:
        style.append("同儕教學：輪流講題與互相提問")
    if energy < 55:
        style.append("作息優先：固定睡眠窗＋晨間例行")
    if mood < 55:
        style.append("情緒調節：呼吸與短寫作 3 分鐘")
    if not style:
        style.append("以做促學：先練題再回整理")

    micro = [
        "每週兩次 45 分鐘深度練習",
        "一頁心智圖回顧本週",
        "安排一次運動或社交補能",
    ]

    parts = [
        f"人格總結：{persona}",
        f"學習風格與策略：\n- " + "\n- ".join(style),
        f"未來兩週微行動：\n- " + "\n- ".join(micro),
        f"(GPA {player.GPA:.2f}｜Mid {player.midterm}｜Final {player.final})",
    ]
    if error:
        parts.append(f"(提示：AI 服務不可用，改用在地建議；{error})")
    return "\n\n".join(parts)
