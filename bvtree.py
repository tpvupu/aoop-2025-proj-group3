import random
import copy

class BehaviorTreePolicy:
    """
    基礎行為樹策略（作為保守平衡型的範例）。
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
        knowledge_target =  week_index * 5  # 簡單線性目標
        if player.knowledge < knowledge_target and "study" in actions:
            return "study"
        
        # 4) 社交補足：社交值過低時優先社交
        if player.social < 30 and "socialize" in actions:
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
        average_attribute = (player.energy + player.mood + player.social) / 3
        
        # 1) 優先處理不足的屬性（< 35）
        if player.energy < 35 and "rest" in actions:
            return "rest"
        if player.social < 35 and "socialize" in actions:
            return "socialize"
        if player.mood < 35 and "play_game" in actions:
            return "play_game"
        

        # 2) 知識補足（較溫和的目標）
        if player.knowledge < week_index * 5 and "study" in actions:
            return "study"
        
        # 進一步處理相對低的屬性（低於平均值2以上）
        if player.energy < average_attribute - 2 and "rest" in actions:
            return "rest"
        if player.mood < average_attribute - 2 and "play_game" in actions:
            return "play_game"
        if player.social < average_attribute - 2 and "socialize" in actions:
            return "socialize"

        
        # 3) 均衡狀態下，輪流做各種行為
        return random.choice(actions)


class AggressivePolicy(BehaviorTreePolicy):
    """
    激進極端型策略：追求極致表現，可能長期專注於單一行為。
    只在數值極低（接近崩潰）時才會切換。
    """
    
    def __init__(self, epsilon: float = 0.05, focus_action: str = None) -> None:
        super().__init__(epsilon)
        # 全域預設（僅在沒有 per-player 設定時使用）
        self.focus_action = focus_action
        # 針對每位玩家的偏好極端行為：{ id(player): action }
        self._focus_for_player: dict[int, str] = {}
    
    def choose(self, player, actions: list[str], week_index: int) -> str:
        """
        激進模式：預設維持單一極端行為（focus_action）。
        若預期下次執行該行為會讓任一屬性變成負數，則改為執行能提升該屬性的動作。
        否則就維持單一行為。
        """

        # 本模式不做隨機探索：持續執行偏好極端行為直到需要修正

        # 依玩家設定或初始化偏好極端行為（首次隨機選一個）
        pid = id(player)
        if pid not in self._focus_for_player or self._focus_for_player[pid] not in actions:
            # 若有外部指定的偏好，優先使用；否則隨機選一個
            self._focus_for_player[pid] = self.focus_action if (self.focus_action in actions) else random.choice(actions)

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


class CasualPolicy(BehaviorTreePolicy):
    """
    隨性自由型策略：更高的隨機性，偶爾跟隨直覺，沒有嚴格計劃。
    只在真的很不舒服時才會調整行為。
    """
    
    def __init__(self, epsilon: float = 0.4) -> None:
        super().__init__(epsilon)

    def choose(self, player, actions: list[str], week_index: int) -> str:
        # 高隨機性探索
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        # 1) 嚴重不適時才會調整行為
        if player.energy < 10 and "rest" in actions:
            return "rest"
        if player.mood < 10 and "play_game" in actions:
            return "play_game"
        if player.social < 10 and "socialize" in actions:
            return "socialize"
        
        # 2) 偶爾讀書，但不強求
        if player.knowledge < week_index * 4 and "study" in actions:
            if random.random() < 0.5:
                return "study"
        
        # 3) 隨性選擇其他行為
        return random.choice(actions)
    


class FSMBehaviorPolicy:
    """
    有限狀態機策略：在三種行為樹之間切換。
    狀態：
    - CONSERVATIVE: 保守平衡型
    - AGGRESSIVE: 激進極端型(讀書模式)
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
        # 強制規則：第 5、6、12、13 週一定執行讀書
        if week_index in [5, 6, 12, 13] and "study" in actions:
            return "study"

        # 依週數套用指定狀態：
        #  - 5,6,12,13 週：AGGRESSIVE（極端讀書）
        #  - 8,9,15,16 週：CASUAL（考後兩週，排除讀書且隨機性較高）
        #  - 其他週：CONSERVATIVE
        self._apply_week_based_state(week_index)

        # 考後兩週的 CASUAL：排除 study 並提高隨機性
        effective_actions = actions
        if self.current_state == "CASUAL" and week_index in [8, 9, 15, 16]:
            filtered = [a for a in actions if a != "study"]
            effective_actions = filtered or actions  # 以免動作集被清空
            # 確保 CASUAL 在這兩週的隨機性較高
            self.states["CASUAL"] = CasualPolicy(epsilon=0.6)

        # 使用當前狀態策略決策
        current_policy = self.states[self.current_state]
        return current_policy.choose(player, effective_actions, week_index)
    
    def _apply_week_based_state(self, week_index: int) -> None:
        """依週數直接指定狀態，符合需求規則。"""
        self.weeks_in_state += 1
        if week_index in [5, 6, 12, 13]:
            # 極端讀書
            if self.current_state != "AGGRESSIVE":
                self._transition_to("AGGRESSIVE")
            # 確保激進策略為讀書偏好
            self.states["AGGRESSIVE"] = AggressivePolicy(epsilon=0.05, focus_action="study")
        elif week_index in [8, 9, 15, 16]:
            # 考後兩週：隨性，且排除讀書（在 choose 時處理）
            if self.current_state != "CASUAL":
                self._transition_to("CASUAL")
            # 提高隨機性
            self.states["CASUAL"] = CasualPolicy(epsilon=0.6)
        else:
            if self.current_state != "CONSERVATIVE":
                self._transition_to("CONSERVATIVE")
    
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
            
            # 如果切換到激進型，指定為讀書型態的極端偏好
            if new_state == "AGGRESSIVE":
                self.states["AGGRESSIVE"] = AggressivePolicy(epsilon=0.05, focus_action="study")
    
    def get_state_stats(self) -> dict:
        """取得狀態統計資訊"""
        return {
            'current_state': self.current_state,
            'weeks_in_current': self.weeks_in_state,
            'transition_history': self.state_history
        }