#!/usr/bin/env python3
"""
單獨測試：激進極端型（AggressivePolicy）策略的模擬結果
- 只執行 AggressivePolicy
- 輸出期中/期末/知識/GPA 統計與圖表
- 圖表與資料輸出到 simulation_plots/激進極端型_policy/
"""

from simulation import Simulation
from bvtree import AggressivePolicy
from character import Bubu, Yier, Mitao, Huihui
import random
import statistics


def run_aggressive_only(n_players: int = 300):
    policy_name = "激進極端型"
    out_dir = f"simulation_plots/{policy_name}_policy"

    print("\n" + "=" * 70)
    print(f"  📊 單獨測試策略：{policy_name}")
    print("=" * 70)

    sim = Simulation(
        n_players=n_players,
        policy=AggressivePolicy(epsilon=0.05),
        out_dir=out_dir,
    )

    print(f"正在模擬 {n_players} 名玩家... ", end="", flush=True)
    sim.run()
    print("✓")

    print("正在生成圖表... ", end="", flush=True)
    sim.plot_midterm_final(title_add=f" ({policy_name})")
    sim.plot_total(title_add=f" ({policy_name})")
    sim.plot_gpa(title_add=f" ({policy_name})")
    sim.export_gpa_csv()
    print("✓")

    # 統計摘要
    midterm_avg = statistics.mean(sim.midterm)
    final_avg = statistics.mean(sim.final)
    knowledge_avg = statistics.mean(sim.knowledge)
    gpa_avg = statistics.mean(sim.gpa)
    gpa_std = statistics.stdev(sim.gpa) if len(sim.gpa) > 1 else 0.0

    print("\n📈 統計結果:")
    print(f"  期中成績: {midterm_avg:6.2f} ± {statistics.stdev(sim.midterm):5.2f}")
    print(f"  期末成績: {final_avg:6.2f} ± {statistics.stdev(sim.final):5.2f}")
    print(f"  知識水平: {knowledge_avg:6.2f} ± {statistics.stdev(sim.knowledge):5.2f}")
    print(f"  GPA平均: {gpa_avg:6.2f} ± {gpa_std:5.2f}")
    print(f"\n💾 圖表與資料已儲存至: {out_dir}/")


if __name__ == "__main__":
    run_aggressive_only(n_players=300)

    # 額外：列出 GPA 前五名的行動序列與每次屬性變化
    def _simulate_player_with_logging(player_cls, policy_factory):
        player = player_cls()
        policy = policy_factory()
        actions = ["study", "rest", "play_game", "socialize"]
        logs = []

        def _log_step(week, action, before, after):
            delta = {
                'mood': after['mood'] - before['mood'],
                'energy': after['energy'] - before['energy'],
                'social': after['social'] - before['social'],
                'knowledge': after['knowledge'] - before['knowledge'],
            }
            logs.append({
                'week': week,
                'action': action,
                'before': before,
                'after': after,
                'delta': delta,
            })

        # 前 7 週
        for _ in range(7):
            week = player.week_number
            action = policy.choose(player, actions, week)
            before = {
                'mood': player.mood,
                'energy': player.energy,
                'social': player.social,
                'knowledge': player.knowledge,
            }
            try:
                getattr(player, action)(1)
            except ZeroDivisionError:
                # 遇到除零，改為休息避免崩潰
                action = 'rest'
                getattr(player, action)(1)
            after = {
                'mood': player.mood,
                'energy': player.energy,
                'social': player.social,
                'knowledge': player.knowledge,
            }
            _log_step(week, action, before, after)
            player.week_number += 1

        player.get_midterm()

        # 後 7 週
        for _ in range(7):
            week = player.week_number
            action = policy.choose(player, actions, week)
            before = {
                'mood': player.mood,
                'energy': player.energy,
                'social': player.social,
                'knowledge': player.knowledge,
            }
            try:
                getattr(player, action)(1)
            except ZeroDivisionError:
                action = 'rest'
                getattr(player, action)(1)
            after = {
                'mood': player.mood,
                'energy': player.energy,
                'social': player.social,
                'knowledge': player.knowledge,
            }
            _log_step(week, action, before, after)
            player.week_number += 1

        player.get_final()
        player.calculate_GPA()

        return {
            'character': player_cls.__name__,
            'gpa': player.GPA,
            'midterm': player.midterm,
            'final': player.final,
            'knowledge': player.knowledge,
            'actions': [entry['action'] for entry in logs],
            'logs': logs,
        }

    def run_aggressive_top5_details(n_players: int = 300):
        print("\n" + "=" * 70)
        print("  🔝 GPA 前五名詳情（AggressivePolicy）")
        print("=" * 70)

        player_classes = [Bubu, Yier, Mitao, Huihui]
        results = []

        for _ in range(n_players):
            cls = random.choice(player_classes)
            res = _simulate_player_with_logging(cls, lambda: AggressivePolicy(epsilon=0.05))
            results.append(res)

        top5 = sorted(results, key=lambda r: r['gpa'], reverse=True)[:5]

        for i, r in enumerate(top5, 1):
            print(f"\n#{i} 角色: {r['character']} | GPA: {r['gpa']:.2f} | 期中: {r['midterm']:.1f} | 期末: {r['final']:.1f} | 知識: {r['knowledge']:.1f}")
            print("選擇策略（行動序列）: ", " → ".join(r['actions']))
            print("每週屬性數值（行動後）:")
            for entry in r['logs']:
                w = entry['week']
                act = entry['action']
                a = entry['after']
                print(
                    f"  W{w:2d} {act:10} | 心情 {int(a['mood']):3d} 體力 {int(a['energy']):3d} 社交 {int(a['social']):3d} 知識 {a['knowledge']:5.1f}"
                )

        print("\n（僅顯示 AggressivePolicy；若需 FSM 狀態轉換詳列，可另加 FSM 版本腳本。）")

    run_aggressive_top5_details(n_players=300)
