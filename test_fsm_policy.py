#!/usr/bin/env python3
"""
單獨測試：FSM（有限狀態機）策略
- 模擬多位玩家僅用 FSMBehaviorPolicy
- 收集每週行動後的屬性數值（心情/體力/社交/知識）與 FSM 狀態
- 輸出 GPA 最高三名與最低三名的每週屬性數值
"""

from bvtree import FSMBehaviorPolicy
from character import Bubu, Yier, Mitao, Huihui
import random
import statistics

ACTIONS = ["study", "rest", "play_game", "socialize"]


def simulate_player_with_weekly_logs(player_cls) -> dict:
    """模擬單一玩家：
    - 前7週行動，然後期中考
    - 後7週行動，然後期末考與 GPA
    - 每週記錄行動後的屬性數值與當週 FSM 狀態
    """
    player = player_cls()
    policy = FSMBehaviorPolicy()  # 每位玩家有獨立的 FSM 狀態機

    weekly = []  # [{week: int, state: str, action: str, mood:int, energy:int, social:int, knowledge:float}]
    actions = []

    def run_one_week():
        week = player.week_number
        action = policy.choose(player, ACTIONS, week)
        # 執行行動（避免除零錯誤）
        try:
            getattr(player, action)(1)
        except ZeroDivisionError:
            # 安全回退：若讀書在某週引發除零，改休息
            action = 'rest'
            getattr(player, action)(1)
        actions.append(action)
        weekly.append({
            'week': len(weekly) + 1,
            'state': policy.current_state,
            'action': action,
            'mood': player.mood,
            'energy': player.energy,
            'social': player.social,
            'knowledge': player.knowledge,
        })
        player.week_number += 1

    # 前7週
    for _ in range(7):
        run_one_week()
    player.get_midterm()

    # 後7週
    for _ in range(7):
        run_one_week()
    player.get_final()
    player.calculate_GPA()

    return {
        'character': player_cls.__name__,
        'gpa': player.GPA,
        'midterm': player.midterm,
        'final': player.final,
        'total_score': player.total_score,
        'weekly': weekly,
        'actions': actions,
    }


def run_fsm_top_bottom(n_players: int = 300):
    print("\n" + "=" * 70)
    print("  🔄 單獨測試：FSM（有限狀態機）")
    print("=" * 70)

    player_classes = [Bubu, Yier, Mitao, Huihui]
    results = []

    print(f"正在模擬 {n_players} 名玩家... ", end="", flush=True)
    for _ in range(n_players):
        cls = random.choice(player_classes)
        res = simulate_player_with_weekly_logs(cls)
        results.append(res)
    print("✓")

    # 取 GPA Top3 與 Bottom3
    sorted_res = sorted(results, key=lambda r: r['gpa'])
    bottom3 = sorted_res[:3]
    top3 = sorted_res[-3:][::-1]

    def print_player_detail(tag: str, r: dict):
        print(f"\n{tag} 角色: {r['character']} | GPA: {r['gpa']:.2f} | 期中: {r['midterm']:.1f} | 期末: {r['final']:.1f}")
        print("行動序列: ", " → ".join(r['actions']))
        print("每週屬性數值（行動後）：")
        for w in r['weekly']:
            print(
                f"  W{w['week']:2d} [{w['state']}] {w['action']:10} | 心情 {w['mood']:3d} 體力 {w['energy']:3d} 社交 {w['social']:3d} 知識 {w['knowledge']:5.1f}"
            )

    print("\n" + "-" * 70)
    print("📈 GPA 最高三名詳情：")
    for i, r in enumerate(top3, 1):
        print_player_detail(f"#{i}", r)

    print("\n" + "-" * 70)
    print("📉 GPA 最低三名詳情：")
    for i, r in enumerate(bottom3, 1):
        print_player_detail(f"#{i}", r)


if __name__ == "__main__":
    run_fsm_top_bottom(n_players=300)
