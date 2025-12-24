#!/usr/bin/env python3
"""
簡單測試 FSM 策略 - 不需要 pygame
直接測試行為樹邏輯
"""

import random
import statistics
from bvtree import (
    BehaviorTreePolicy,
    ConservativePolicy, 
    AggressivePolicy, 
    CasualPolicy,
    FSMBehaviorPolicy
)


class SimpleCharacter:
    """簡化版角色，用於測試策略"""
    def __init__(self, intelligence=70, mood=75, energy=90, social=30):
        self.intelligence = intelligence
        self.mood = mood
        self.energy = energy
        self.social = social
        self.knowledge = 0.0
        self.week_number = 0
    
    def study(self, degree=1):
        growth = int(
            self.intelligence * 0.11 +
            self.mood * 0.05 +
            self.energy * 0.08 +
            self.social * 0.03
        )
        self.mood = max(0, self.mood - int(growth*0.8*degree))
        self.energy = max(0, self.energy - int(growth*0.5*degree) - 3)
        self.knowledge = min(100, self.knowledge + growth + 1)
    
    def rest(self, degree=1):
        growth = int(
            (100 - self.energy) * 0.15 +
            (100 - self.mood) * 0.02 +
            (self.intelligence - 50) * 0.2 -
            (self.social - 30) * 0.01
        )
        self.mood = min(100, self.mood + int(growth*0.6*degree))
        self.energy = min(100, self.energy + growth*degree)
        self.knowledge = min(100, self.knowledge + 2)
    
    def play_game(self, degree=1):
        growth = int(
            (100 - self.mood) * 0.2 +
            (self.intelligence - 30) * 0.02 +
            self.energy * 0.01 -
            self.social * 0.01
        )
        self.mood = min(100, self.mood + growth*degree)
        self.energy = max(0, self.energy + int(growth*0.2*degree))
        self.knowledge = min(100, self.knowledge + 1)
    
    def socialize(self, degree=1):
        growth = int(
            (self.social - 30) * 0.1 +
            (self.mood - 50) * 0.03 +
            self.energy * 0.01
        )
        self.mood = min(100, self.mood + 4*degree)
        self.energy = max(0, self.energy - 5*degree)
        self.social = min(100, self.social + growth*degree)
        self.knowledge = min(100, self.knowledge + 4)


def test_policy_behavior(policy, policy_name):
    """測試單一策略的行為模式"""
    print(f"\n{'='*70}")
    print(f"測試策略：{policy_name}")
    print(f"{'='*70}")
    
    player = SimpleCharacter()
    actions = ["study", "rest", "play_game", "socialize"]
    action_history = []
    
    print(f"\n初始狀態: 知識={player.knowledge:.1f}, 心情={player.mood}, "
          f"體力={player.energy}, 社交={player.social}")
    
    # 模擬 16 週
    for week in range(16):
        action = policy.choose(player, actions, week)
        action_history.append(action)
        getattr(player, action)(1)
        player.week_number = week + 1
        
        # 每 4 週顯示一次狀態
        if (week + 1) % 4 == 0:
            print(f"\nWeek {week + 1} - 行動: {action}")
            print(f"  狀態: 知識={player.knowledge:.1f}, 心情={player.mood}, "
                  f"體力={player.energy}, 社交={player.social}")
    
    # 統計行為分佈
    from collections import Counter
    action_counts = Counter(action_history)
    print(f"\n行為統計（16週）:")
    for action, count in sorted(action_counts.items(), key=lambda x: -x[1]):
        percentage = count / 16 * 100
        bar = '█' * int(percentage / 5)
        print(f"  {action:12} : {count:2} 次 ({percentage:5.1f}%) {bar}")
    
    print(f"\n最終狀態: 知識={player.knowledge:.1f}, 心情={player.mood}, "
          f"體力={player.energy}, 社交={player.social}")
    
    return player.knowledge


def test_fsm_transitions():
    """詳細測試 FSM 的狀態轉換"""
    print(f"\n{'='*70}")
    print(f"測試 FSM 狀態轉換機制")
    print(f"{'='*70}")
    
    fsm = FSMBehaviorPolicy(initial_state="CONSERVATIVE")
    player = SimpleCharacter()
    actions = ["study", "rest", "play_game", "socialize"]
    
    print(f"\n初始狀態: {fsm.current_state}")
    print(f"玩家初始值: 知識={player.knowledge:.1f}, 心情={player.mood}, "
          f"體力={player.energy}, 社交={player.social}")
    
    prev_state = fsm.current_state
    
    for week in range(16):
        action = fsm.choose(player, actions, week)
        getattr(player, action)(1)
        player.week_number = week + 1
        
        # 檢測狀態變化
        if fsm.current_state != prev_state:
            print(f"\n  【狀態轉換】Week {week + 1}: {prev_state} → {fsm.current_state}")
            print(f"    觸發原因: 知識={player.knowledge:.1f}, 心情={player.mood}, "
                  f"體力={player.energy}, 社交={player.social}")
            print(f"    下一步行動: {action}")
            prev_state = fsm.current_state
        elif week in [0, 7, 14, 15]:  # 關鍵週顯示狀態
            print(f"\n  Week {week + 1}: 維持 {fsm.current_state} 狀態")
            print(f"    行動: {action}, 知識={player.knowledge:.1f}, "
                  f"心情={player.mood}, 體力={player.energy}")
    
    print(f"\n最終狀態: {fsm.current_state}")
    print(f"總共轉換次數: {len(fsm.state_history)}")
    
    if fsm.state_history:
        print(f"\n狀態轉換歷史:")
        for i, trans in enumerate(fsm.state_history, 1):
            print(f"  {i}. {trans['from']} → {trans['to']} "
                  f"(停留 {trans['weeks_stayed']} 週)")


def compare_policies():
    """比較所有策略的最終知識水平"""
    print(f"\n{'='*70}")
    print(f"比較所有策略的效果（模擬100次取平均）")
    print(f"{'='*70}\n")
    
    policies = {
        "保守平衡型": ConservativePolicy(epsilon=0.1),
        "激進極端型": AggressivePolicy(epsilon=0.05),
        "隨性自由型": CasualPolicy(epsilon=0.4),
        "有限狀態機": FSMBehaviorPolicy(),
        "基礎行為樹": BehaviorTreePolicy(epsilon=0.1)
    }
    
    results = {}
    
    for name, policy_class in policies.items():
        knowledge_scores = []
        mood_scores = []
        energy_scores = []
        
        for _ in range(100):
            # 每次創建新的策略實例（避免狀態污染）
            if name == "保守平衡型":
                policy = ConservativePolicy(epsilon=0.1)
            elif name == "激進極端型":
                policy = AggressivePolicy(epsilon=0.05)
            elif name == "隨性自由型":
                policy = CasualPolicy(epsilon=0.4)
            elif name == "有限狀態機":
                policy = FSMBehaviorPolicy()
            else:
                policy = BehaviorTreePolicy(epsilon=0.1)
            
            player = SimpleCharacter()
            actions = ["study", "rest", "play_game", "socialize"]
            
            for week in range(16):
                action = policy.choose(player, actions, week)
                getattr(player, action)(1)
                player.week_number = week + 1
            
            knowledge_scores.append(player.knowledge)
            mood_scores.append(player.mood)
            energy_scores.append(player.energy)
        
        results[name] = {
            'knowledge': statistics.mean(knowledge_scores),
            'knowledge_std': statistics.stdev(knowledge_scores),
            'mood': statistics.mean(mood_scores),
            'energy': statistics.mean(energy_scores)
        }
    
    # 顯示結果表格
    print(f"{'策略':12} {'知識':>8} {'±':^5} {'心情':>8} {'體力':>8}")
    print("-" * 60)
    
    for name, stats in sorted(results.items(), key=lambda x: -x[1]['knowledge']):
        print(f"{name:12} {stats['knowledge']:8.2f} ± {stats['knowledge_std']:3.1f}   "
              f"{stats['mood']:8.2f} {stats['energy']:8.2f}")
    
    # 找出最佳策略
    best = max(results.items(), key=lambda x: x[1]['knowledge'])
    most_stable = min(results.items(), key=lambda x: x[1]['knowledge_std'])
    
    print(f"\n🏆 知識獲得最高: {best[0]} (平均 {best[1]['knowledge']:.2f})")
    print(f"📊 表現最穩定: {most_stable[0]} (標準差 {most_stable[1]['knowledge_std']:.2f})")


if __name__ == "__main__":
    # 1. 測試各個策略的行為模式
    print("\n" + "="*70)
    print(" 行為樹策略測試系統 ".center(70, "="))
    print("="*70)
    
    test_policy_behavior(ConservativePolicy(epsilon=0.1), "保守平衡型")
    test_policy_behavior(AggressivePolicy(epsilon=0.05), "激進極端型")
    test_policy_behavior(CasualPolicy(epsilon=0.4), "隨性自由型")
    
    # 2. 測試 FSM 狀態轉換
    test_fsm_transitions()
    
    # 3. 比較所有策略
    compare_policies()
    
    print(f"\n{'='*70}")
    print(" 測試完成！ ".center(70, "="))
    print(f"{'='*70}\n")
