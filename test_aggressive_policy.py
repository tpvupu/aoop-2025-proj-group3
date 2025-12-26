#!/usr/bin/env python3
"""
單獨測試：激進極端型（AggressivePolicy）策略的模擬結果
- 只執行 AggressivePolicy
- 輸出期中/期末/知識/GPA 統計與圖表
- 圖表與資料輸出到 simulation_plots/激進極端型_policy/
"""

from simulation import Simulation
from bvtree import AggressivePolicy
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
