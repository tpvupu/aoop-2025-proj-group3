# AI 行為決策系統說明文件

## 📚 系統架構

本專案實作了一個**有限狀態機（FSM）** + **行為樹（Behavior Tree）**的混合 AI 決策系統，用於模擬學生在學期中如何決定每週的行動（讀書、休息、玩遊戲、社交）。

---
OpenAI Key
```
export OPENAI_API_KEY="your_api_key_here"
```
---

## 🌲 三種行為樹策略

### 🛡️ 保守平衡型（Conservative Policy）
**特性：** 維持各項數值均衡，避免任何屬性過低或過高

**決策邏輯：**
優先級從高到低：
1. 任一屬性 < 35 → 緊急補救
```python
if player.energy < 35 and "rest" in actions:
            return "rest"
        if player.social < 35 and "socialize" in actions:
            return "socialize"
        if player.mood < 35 and "play_game" in actions:
            return "play_game"
```
2. 知識未達目標 (週數*5) → 讀書
```python
if player.knowledge < week_index * 5 and "study" in actions:
            return "study"
```
3. 處理相對低的屬性（低於平均值2以上）
```python
if player.energy < average_attribute - 2 and "rest" in actions:
            return "rest"
        if player.mood < average_attribute - 2 and "play_game" in actions:
            return "play_game"
        if player.social < average_attribute - 2 and "socialize" in actions:
            return "socialize"
```
4. 均衡狀態 → 隨機行為
```python
return random.choice(actions)
```


**參數：**
- `epsilon = 0.1`（10% 機率隨機選擇）

**適合情境：**
- 追求穩定發展
- 不想冒險，保守型人格
- 各項屬性都不能太差

---

### 🗡️ 激進極端型（AggressivePolicy）
**特性：** 長期專注單一行為，只在數值極低（接近崩潰）時才會切換。

**決策邏輯：**
1. 隨機選擇一個動作作為此玩家長期專注的行為
```python
pid = id(player)
if pid not in self._focus_for_player or self._focus_for_player[pid] not in actions:
    self._focus_for_player[pid] = self.focus_action if (self.focus_action in actions) else random.choice(actions)
# 若有外部指定的偏好，優先使用；否則隨機選一個
```
2. 若預期下次執行該行為會讓任一屬性變成負數，則改為執行能提升該屬性的動作。
```python
 # 預測執行單一行為後是否會讓屬性為負
        def would_cause_negative(action_name: str):
            """模擬執行 action，一旦未經 clamp 的預測值會落到 < 0，視為不安全。
            以 before_value + last_week_change 作為未經 clamp 的預測。
            """
            try:
                simulated = copy.deepcopy(player)
                before = {
                    'mood': simulated.mood,
                    'energy': simulated.energy,
                    'social': simulated.social,
                }
                getattr(simulated, action_name)(1)
                # last_week_change = [mood_delta, energy_delta, social_delta, knowledge_delta]
                lwc = simulated.last_week_change if hasattr(simulated, 'last_week_change') else [0,0,0,0]
                projected = {
                    'mood': before['mood'] + (lwc[0] if len(lwc) > 0 else 0),
                    'energy': before['energy'] + (lwc[1] if len(lwc) > 1 else 0),
                    'social': before['social'] + (lwc[2] if len(lwc) > 2 else 0),
                }
                risky = any(v < 0 for v in projected.values())
                # 若行為本身會造成負值，傳回模擬資料供後續判定目標屬性
                simulated._projected = projected
                return risky, simulated
            except Exception:
                # 任何異常（如除零）視為不安全
                return True, None
         focus_action = self._focus_for_player[pid]
        risky, simulated_player = would_cause_negative(focus_action)

        # 若不安全，選擇能提升對應屬性的行動（優先處理最接近負值者）
        if risky:
            # 找出哪個屬性會變成負值（用未經 clamp 的 projected 判斷），針對該屬性選擇修正行為
            target_attr = None
            target_val = 0
            if simulated_player is not None and hasattr(simulated_player, '_projected'):
                projected = simulated_player._projected
                negatives = {k: v for k, v in projected.items() if v < 0}
                if negatives:
                    # 選擇最負的那個屬性做修正
                    target_attr, target_val = min(negatives.items(), key=lambda kv: kv[1])
            # 映射修正行為
            if target_attr == 'energy' and 'rest' in actions:
                return 'rest'
            if target_attr == 'mood' and 'play_game' in actions:
                return 'play_game'
            if target_attr == 'social' and 'socialize' in actions:
                return 'socialize'
            # 若無法判定或模擬失敗，依當前屬性最小值進行修正
            if player.energy <= player.mood and player.energy <= player.social and 'rest' in actions:
                return 'rest'
            if player.mood <= player.energy and player.mood <= player.social and 'play_game' in actions:
                return 'play_game'
            if 'socialize' in actions:
                return 'socialize'
            # 若沒有對應補救行為，退回可用行為之一
            return random.choice(actions)

        # 安全：維持單一極端行為
        return focus_action
```

**參數：**
- `epsilon = 0.05`（5% 隨機探索，極低）
- `focus_action`（可指定偏好行為）

**適合情境：**
- 追求最高成績
- 接受犧牲其他屬性
- 有明確目標的積極型人格


---

### 💭 隨性自由型（CasualPolicy）
**特性：** 高隨機性，跟隨直覺，沒有嚴格計劃

**決策邏輯：**
1. 高隨機性探索(不根據此策略行動)
```python
    if random.random() < self.epsilon:
        return random.choice(actions)
    # epsilon = 0.4（40% 隨機探索，最高）
```
2. 處理相對低的屬性（低於10以下）
```python
 if player.energy < 10 and "rest" in actions:
            return "rest"
        if player.mood < 10 and "play_game" in actions:
            return "play_game"
        if player.social < 10 and "socialize" in actions:
            return "socialize"
```
3.  讀書是「可有可無」而且是隨機的，知識未達目標 (週數*5) → 概率性讀書
```python
if player.knowledge < week_index * 4 and "study" in actions:
            if random.random() < 0.5:
                return "study"
```
4. 隨機行動
```python
 return random.choice(actions)
```


**參數：**
- `epsilon = 0.4`（40% 隨機探索，最高）

**適合情境：**
- 享受過程，不追求極致
- 看心情做事
- 自由散漫型人格


---

### ⏰ 有限狀態機（FSMBehaviorPolicy）

#### 核心概念
FSM 會在三種行為樹之間**動態切換**，根據玩家當前狀態和週數自動調整策略。

#### 狀態轉換圖
```
         壓力低 & 狀態良好
    ┌───────────────────────┐
    │                       ↓
CONSERVATIVE ←───────→ AGGRESSIVE
 (保守平衡)             (激進極端讀書)
    ↑                       ↓
    │   考試後放鬆           │ 考試前衝刺
    └──────── CASUAL ←──────┘
              (隨性自由)
```

#### 狀態轉換條件

#### CONSERVATIVE → AGGRESSIVE
- 考試前兩週（week 6, 7, 14, 15）
- **意義：** 考試週前的衝刺
```python
if week_index in [6, 7, 13, 14]:
    if self.current_state != "AGGRESSIVE":
        self._transition_to("AGGRESSIVE")
    self.states["AGGRESSIVE"] = AggressivePolicy(epsilon=0.05, focus_action="study")

```
#### AGGRESSIVE → CASUAL
- 考試後兩週
- **意義：** 考試週後放鬆一下，恢復狀態
```python
elif week_index in [9, 10]:
    if self.current_state != "CASUAL":
        self._transition_to("CASUAL")
    self.states["CASUAL"] = CasualPolicy(epsilon=0.6)
```

#### CONSERVATIVE
- 其餘時間
- **意義：** 維持個數值的基本狀態
```python
else:
    if self.current_state != "CONSERVATIVE":
        self._transition_to("CONSERVATIVE")
```
 **特點：** 平衡了知識與身心健康

**適合情境** 
- 具有明確學習節奏
- 習慣以「階段目標」規劃學習與生活
- 考前能夠高度專注的學生



---

## 📊 五種策略模擬結果比較

| 策略 | 期中 | 期末 | 知識 | GPA | 標準差 |
|------|------|------|------|-----|--------|
| Conservative | 72.89 | 80.73 | 74.54 | 3.69 | 0.11 |
| Aggressive | 64.96 | 57.64 | 37.22 | 2.73 | 0.95 |
| Casual | 73.83 | 78.38 | 74.37 | 3.66 | 0.31 |
| FSM | 82.90 | 88.70 | 95.19 | 4.13 | 0.08 |

🏆 **最高平均 GPA:** FSM (4.13)  
📚 **最高知識值:** FSM (95.19)  
📈 **最穩定策略:** FSM (標準差 0.08)

💡 **策略特點分析：**

- **保守平衡型（Conservative）**：  
  各項屬性均衡，心情體力最好，但成績較低

- **激進極端型（Aggressive）**：  
  知識最高，可能達到滿分，但心情體力會很差

- **隨性自由型（Casual）**：  
  變化最大，享受過程，成績中等

- **有限狀態機（FSM）**：  
  動態調整，平衡成績與身心狀態，整體表現最佳，最推薦



---
