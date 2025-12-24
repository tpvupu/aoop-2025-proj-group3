import random


class BehaviorTreePolicy:
    """
    基礎行為樹策略（保守平衡型）。
    Priority (高 -> 低)：
    1) 體力過低先休息
    2) 心情過低先玩遊戲
    3) 知識未達當前週目標先讀書
    4) 社交補足
    5) 其餘情況做一個輕度探索的隨機行動
    """

    def __init__(self, epsilon: float = 0.1) -> None:
        self.epsilon = epsilon  # 少量隨機，避免僵化行為

    def choose(self, player, actions: list[str], week_index: int) -> str:
        # 探索：偶爾亂選，讓分佈更自然
        if random.random() < self.epsilon:
            return random.choice(actions)

        # 1) 低體力：先休息
        if player.energy < 35 and "rest" in actions:
            return "rest"

        # 2) 低心情：先玩遊戲提 mood
        if player.mood < 45 and "play_game" in actions:
            return "play_game"

        # 3) 知識追目標：越接近期中/期末越想讀書
        knowledge_target = 20 + week_index * 3  # 簡單線性目標
        if player.knowledge < knowledge_target and "study" in actions:
            return "study"

        # 4) 社交補足
        if player.social < 40 and "socialize" in actions:
            return "socialize"

        # 5) 其餘：在可用行為中擇一（偏好讀書/社交）
        preferred = [a for a in ["study", "socialize", "rest", "play_game"] if a in actions]
        return random.choice(preferred or actions)


class ConservativePolicy(BehaviorTreePolicy):
    """
    保守平衡型策略：維持各項數值均衡，不讓任何屬性過低或過高。
    更積極地維護各項數值在健康範圍內。
    """
    
    def choose(self, player, actions: list[str], week_index: int) -> str:
        # 少量隨機探索
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        # 計算各項數值偏離平衡點的程度（目標：60左右）
        energy_deficit = 60 - player.energy
        mood_deficit = 60 - player.mood
        social_deficit = 60 - player.social
        knowledge_target = 25 + week_index * 2.5
        knowledge_deficit = knowledge_target - player.knowledge
        
        # 1) 優先處理嚴重不足的屬性（< 40）
        if player.energy < 40 and "rest" in actions:
            return "rest"
        if player.mood < 40 and "play_game" in actions:
            return "play_game"
        if player.social < 35 and "socialize" in actions:
            return "socialize"
        
        # 2) 次要處理中等不足的屬性（< 55）
        if player.energy < 55 and energy_deficit > max(mood_deficit, social_deficit, knowledge_deficit) and "rest" in actions:
            return "rest"
        if player.mood < 55 and mood_deficit > max(energy_deficit, social_deficit, knowledge_deficit) and "play_game" in actions:
            return "play_game"
        if player.social < 50 and social_deficit > max(energy_deficit, mood_deficit, knowledge_deficit) and "socialize" in actions:
            return "socialize"
        
        # 3) 知識補足（較溫和的目標）
        if knowledge_deficit > 0 and "study" in actions:
            return "study"
        
        # 4) 均衡狀態下，輪流做各種行為
        return random.choice(actions)


class AggressivePolicy(BehaviorTreePolicy):
    """
    激進極端型策略：追求極致表現，可能長期專注於單一行為。
    只在數值極低（接近崩潰）時才會切換。
    """
    
    def __init__(self, epsilon: float = 0.05, focus_action: str = None) -> None:
        super().__init__(epsilon)
        # 可以指定偏好的極端行為，若無則隨機選一個
        self.focus_action = focus_action
        self.commitment_counter = 0  # 追蹤連續執行同一行為的次數
    
    def choose(self, player, actions: list[str], week_index: int) -> str:
        # 極低隨機性
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        # 1) 緊急狀態：任一屬性 < 20，必須立即處理
        if player.energy < 20 and "rest" in actions:
            self.commitment_counter = 0
            return "rest"
        if player.mood < 25 and "play_game" in actions:
            self.commitment_counter = 0
            return "play_game"
        
        # 2) 期中/期末前衝刺知識（week 6-7 或 13-14）
        if week_index in [6, 7, 13, 14]:
            if player.knowledge < 70 and "study" in actions:
                self.commitment_counter += 1
                return "study"
        
        # 3) 選擇或維持極端策略
        if self.focus_action is None:
            # 根據當前狀態決定要極端追求什麼
            if player.intelligence > 80 or week_index < 8:
                self.focus_action = "study"  # 學霸模式
            elif player.mood < 50:
                self.focus_action = "play_game"  # 娛樂至上
            else:
                self.focus_action = random.choice(["study", "socialize"])
        
        # 4) 執行極端策略（連續做同一件事）
        if self.focus_action in actions:
            self.commitment_counter += 1
            # 每10次行動，5%機會換個極端策略
            if self.commitment_counter > 10 and random.random() < 0.05:
                self.focus_action = random.choice([a for a in actions if a != self.focus_action])
                self.commitment_counter = 0
            return self.focus_action
        
        return random.choice(actions)


class CasualPolicy(BehaviorTreePolicy):
    """
    隨性自由型策略：更高的隨機性，偶爾跟隨直覺，沒有嚴格計劃。
    只在真的很不舒服時才會調整行為。
    """
    
    def __init__(self, epsilon: float = 0.4) -> None:
        super().__init__(epsilon)
        self.mood_weight = random.uniform(0.3, 0.7)  # 隨機生成個性化權重
    
    def choose(self, player, actions: list[str], week_index: int) -> str:
        # 高隨機性：40% 機會完全隨機
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        # 1) 只在真的受不了時才處理（閾值更低）
        if player.energy < 25 and random.random() < 0.7 and "rest" in actions:
            return "rest"
        if player.mood < 30 and random.random() < 0.8 and "play_game" in actions:
            return "play_game"
        
        # 2) 期中期末前一週，可能會臨時抱佛腳（但不一定）
        if week_index in [7, 14] and random.random() < 0.6 and "study" in actions:
            return "study"
        
        # 3) 根據「心情」隨性選擇
        if player.mood > 70:
            # 心情好時更願意社交或玩
            preferred = [a for a in ["socialize", "play_game", "study"] if a in actions]
        elif player.mood < 40:
            # 心情差時想休息或玩
            preferred = [a for a in ["rest", "play_game"] if a in actions]
        else:
            # 普通心情，什麼都行
            preferred = actions
        
        # 4) 加入一些「看心情」的隨機性
        weights = []
        for action in preferred:
            if action == "play_game":
                weights.append(1.5)  # 稍微偏愛娛樂
            elif action == "socialize":
                weights.append(1.2)  # 次要偏愛社交
            else:
                weights.append(1.0)
        
        return random.choices(preferred, weights=weights)[0]


class FSMBehaviorPolicy:
    """
    有限狀態機策略：在三種行為樹之間切換。
    狀態：
    - CONSERVATIVE: 保守平衡型
    - AGGRESSIVE: 激進極端型
    - CASUAL: 隨性自由型
    
    轉換條件基於角色當前狀態和週數。
    """
    
    def __init__(self, initial_state: str = None) -> None:
        self.states = {
            "CONSERVATIVE": ConservativePolicy(epsilon=0.1),
            "AGGRESSIVE": AggressivePolicy(epsilon=0.05),
            "CASUAL": CasualPolicy(epsilon=0.4)
        }
        # 初始狀態：若未指定則隨機選一個
        self.current_state = initial_state or random.choice(list(self.states.keys()))
        self.weeks_in_state = 0  # 在當前狀態已經待了幾週
        self.state_history = []  # 記錄狀態轉換歷史
    
    def choose(self, player, actions: list[str], week_index: int) -> str:
        # 每週更新一次狀態（在新的一週開始時檢查是否要切換）
        self._update_state(player, week_index)
        
        # 使用當前狀態的策略來選擇行為
        current_policy = self.states[self.current_state]
        return current_policy.choose(player, actions, week_index)
    
    def _update_state(self, player, week_index: int) -> None:
        """根據玩家狀態和週數決定是否切換策略"""
        self.weeks_in_state += 1
        
        # 計算當前壓力指數
        stress_level = self._calculate_stress(player, week_index)
        
        # 狀態轉換邏輯
        if self.current_state == "CONSERVATIVE":
            # 保守型 -> 激進型：考試週來臨且知識不足
            if week_index in [6, 7, 13, 14] and player.knowledge < 40:
                self._transition_to("AGGRESSIVE")
            # 保守型 -> 隨性型：狀態良好且壓力低
            elif stress_level < 0.3 and self.weeks_in_state > 2:
                if random.random() < 0.3:
                    self._transition_to("CASUAL")
        
        elif self.current_state == "AGGRESSIVE":
            # 激進型 -> 保守型：壓力過大（任一屬性過低）
            if stress_level > 0.7:
                self._transition_to("CONSERVATIVE")
            # 激進型 -> 隨性型：考試結束，放鬆一下
            elif week_index in [8, 9, 15, 16] and random.random() < 0.4:
                self._transition_to("CASUAL")
        
        elif self.current_state == "CASUAL":
            # 隨性型 -> 保守型：發現狀態失衡
            if stress_level > 0.6:
                self._transition_to("CONSERVATIVE")
            # 隨性型 -> 激進型：考前突然想認真
            elif week_index in [5, 6, 12, 13] and random.random() < 0.25:
                self._transition_to("AGGRESSIVE")
            # 隨性型內部：待太久了可能換心情
            elif self.weeks_in_state > 4 and random.random() < 0.2:
                new_state = random.choice(["CONSERVATIVE", "AGGRESSIVE"])
                self._transition_to(new_state)
    
    def _calculate_stress(self, player, week_index: int) -> float:
        """計算當前壓力程度 (0-1)"""
        # 各項數值不足造成的壓力
        energy_stress = max(0, (40 - player.energy) / 40)
        mood_stress = max(0, (40 - player.mood) / 40)
        social_stress = max(0, (30 - player.social) / 30)
        
        # 知識不足的壓力（考試週加重）
        knowledge_target = 30 + week_index * 2
        knowledge_stress = max(0, (knowledge_target - player.knowledge) / knowledge_target)
        if week_index in [7, 8, 14, 15]:
            knowledge_stress *= 1.5
        
        # 綜合壓力
        total_stress = (energy_stress + mood_stress + social_stress + knowledge_stress) / 4
        return min(1.0, total_stress)
    
    def _transition_to(self, new_state: str) -> None:
        """切換到新狀態"""
        if new_state != self.current_state:
            self.state_history.append({
                'from': self.current_state,
                'to': new_state,
                'weeks_stayed': self.weeks_in_state
            })
            self.current_state = new_state
            self.weeks_in_state = 0
            
            # 如果切換到激進型，重置其內部狀態
            if new_state == "AGGRESSIVE":
                self.states["AGGRESSIVE"] = AggressivePolicy(epsilon=0.05)
    
    def get_state_stats(self) -> dict:
        """取得狀態統計資訊"""
        return {
            'current_state': self.current_state,
            'weeks_in_current': self.weeks_in_state,
            'transition_history': self.state_history
        }