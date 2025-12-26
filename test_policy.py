#!/usr/bin/env python3
"""
測試有限狀態機（FSM）行為策略
展示三種不同的行為樹策略如何影響模擬結果

策略說明：
- 保守平衡型：維持各項數值均衡，不讓任何屬性過低
- 激進極端型：追求極致，可能連續讀書或玩遊戲
- 隨性自由型：高隨機性，根據心情選擇偏好行為
- 有限狀態機：在上述三種策略間動態切換
"""

from simulation import Simulation
from bvtree import (
    ConservativePolicy, 
    AggressivePolicy, 
    CasualPolicy,
    FSMBehaviorPolicy
)
from character import Bubu, Yier, Mitao, Huihui
import random
import statistics
from collections import Counter


def test_single_policy(policy, policy_name, n_players=300):
    """測試單一策略的效果"""
    print(f"\n{'='*70}")
    print(f"  📊 測試策略：{policy_name}")
    print(f"{'='*70}")
    
    out_dir = f"simulation_plots/{policy_name}_policy"
    sim = Simulation(
        n_players=n_players,
        policy=policy,
        out_dir=out_dir
    )
    
    print(f"正在模擬 {n_players} 名玩家... ", end='', flush=True)
    sim.run()
    print("✓")
    
    print(f"正在生成圖表... ", end='', flush=True)
    sim.plot_midterm_final()
    sim.plot_total()
    sim.plot_gpa()
    sim.export_gpa_csv()
    print("✓")
    
    # 顯示統計結果
    print(f"\n📈 統計結果:")
    print(f"  期中成績: {statistics.mean(sim.midterm):6.2f} ± {statistics.stdev(sim.midterm):5.2f}")
    print(f"  期末成績: {statistics.mean(sim.final):6.2f} ± {statistics.stdev(sim.final):5.2f}")
    print(f"  知識水平: {statistics.mean(sim.knowledge):6.2f} ± {statistics.stdev(sim.knowledge):5.2f}")
    print(f"  GPA平均: {statistics.mean(sim.gpa):6.2f} ± {statistics.stdev(sim.gpa):5.2f}")
    print(f"\n💾 圖表已儲存至: {out_dir}/")
    
    return {
        'midterm': statistics.mean(sim.midterm),
        'final': statistics.mean(sim.final),
        'knowledge': statistics.mean(sim.knowledge),
        'gpa': statistics.mean(sim.gpa),
        'gpa_std': statistics.stdev(sim.gpa)
    }


def test_fsm_policy_with_details():
    """測試 FSM 策略並顯示狀態轉換細節"""
    print(f"\n{'='*70}")
    print(f"  🔄 測試策略：有限狀態機（FSM）- 動態切換")
    print(f"{'='*70}")
    
    # 建立一個 FSM 策略實例並追蹤一個玩家的狀態轉換
    fsm_policy = FSMBehaviorPolicy(initial_state="CONSERVATIVE")
    player = Bubu()
    
    print(f"\n🎯 追蹤 {player.chname}（{player.name}）的策略狀態轉換：")
    print(f"   初始狀態: {fsm_policy.current_state}")
    print(f"   初始屬性: 知識={player.knowledge:.1f}, 心情={player.mood}, "
          f"體力={player.energy}, 社交={player.social}\n")
    
    # 模擬 16 週的遊戲
    action_history = []
    prev_state = fsm_policy.current_state
    
    print("週數  狀態變化                   行動         屬性變化")
    print("-" * 70)
    
    for week in range(16):
        action = fsm_policy.choose(player, ["study", "rest", "play_game", "socialize"], week)
        action_history.append(action)
        
        # 記錄執行前的狀態
        old_knowledge = player.knowledge
        
        getattr(player, action)(1)
        player.week_number += 1
        
        # 檢測狀態變化
        state_change = ""
        if fsm_policy.current_state != prev_state:
            state_change = f"  {prev_state} → {fsm_policy.current_state}"
            prev_state = fsm_policy.current_state
        
        # 格式化輸出
        action_cn = {
            'study': '讀書📚',
            'rest': '休息😴',
            'play_game': '玩遊戲🎮',
            'socialize': '社交🤝'
        }
        
        print(f"W{week+1:2}   {state_change:26}  {action_cn.get(action, action):8}  "
              f"知識:{player.knowledge:4.1f} 心情:{player.mood:3} "
              f"體力:{player.energy:3} 社交:{player.social:3}")
    
    print(f"\n✓ 最終狀態: {fsm_policy.current_state}")
    print(f"✓ 狀態轉換次數: {len(fsm_policy.state_history)}")
    
    if fsm_policy.state_history:
        print(f"\n📜 狀態轉換歷史:")
        for i, trans in enumerate(fsm_policy.state_history, 1):
            print(f"   {i}. {trans['from']:12} → {trans['to']:12} (停留 {trans['weeks_stayed']} 週)")
    
    # 統計各行為的執行次數
    action_counts = Counter(action_history)
    print(f"\n📊 行為統計（16週）:")
    
    action_names = {
        'study': '讀書📚',
        'rest': '休息😴',
        'play_game': '玩遊戲🎮',
        'socialize': '社交🤝'
    }
    
    for action in ['study', 'socialize', 'rest', 'play_game']:
        if action in action_counts:
            count = action_counts[action]
            percentage = count / 16 * 100
            bar = '█' * int(percentage / 5)
            print(f"   {action_names.get(action, action):8} : {count:2} 次 ({percentage:5.1f}%) {bar}")
    
    # 跑完整模擬
    print(f"\n{'='*70}")
    print(f"執行完整模擬（300 名玩家）... ", end='', flush=True)
    
    out_dir = "simulation_plots/FSM_policy"
    sim = Simulation(
        n_players=300,
        policy=FSMBehaviorPolicy(),
        out_dir=out_dir
    )
    
    sim.run()
    print("✓")
    
    print(f"正在生成圖表... ", end='', flush=True)
    sim.plot_midterm_final(title_add=" (FSM Policy)")
    sim.plot_total(title_add=" (FSM Policy)")
    sim.plot_gpa(title_add=" (FSM Policy)")
    sim.export_gpa_csv()
    print("✓")
    
    print(f"\n📈 統計結果:")
    print(f"  期中成績: {statistics.mean(sim.midterm):6.2f} ± {statistics.stdev(sim.midterm):5.2f}")
    print(f"  期末成績: {statistics.mean(sim.final):6.2f} ± {statistics.stdev(sim.final):5.2f}")
    print(f"  知識水平: {statistics.mean(sim.knowledge):6.2f} ± {statistics.stdev(sim.knowledge):5.2f}")
    print(f"  GPA平均: {statistics.mean(sim.gpa):6.2f} ± {statistics.stdev(sim.gpa):5.2f}")
    print(f"\n💾 圖表已儲存至: {out_dir}/")
    
    return {
        'midterm': statistics.mean(sim.midterm),
        'final': statistics.mean(sim.final),
        'knowledge': statistics.mean(sim.knowledge),
        'gpa': statistics.mean(sim.gpa),
        'gpa_std': statistics.stdev(sim.gpa)
    }


def compare_all_policies():
    """比較所有策略的效果"""
    print(f"\n{'='*70}")
    print(f"  📊 策略效果總比較（各模擬 300 名玩家）")
    print(f"{'='*70}\n")
    
    policies = {
        "Conservative": ConservativePolicy(epsilon=0.1),
        "Aggressive": AggressivePolicy(epsilon=0.05),
        "Casual": CasualPolicy(epsilon=0.4),
        "FSM": FSMBehaviorPolicy()
    }
    
    results = {}
    
    for name, policy in policies.items():
        print(f"正在模擬 {name}... ", end='', flush=True)
        sim = Simulation(n_players=300, policy=policy)
        sim.run()
        print("✓")
        
        results[name] = {
            'midterm': statistics.mean(sim.midterm),
            'final': statistics.mean(sim.final),
            'knowledge': statistics.mean(sim.knowledge),
            'gpa': statistics.mean(sim.gpa),
            'gpa_std': statistics.stdev(sim.gpa) if len(sim.gpa) > 1 else 0
        }
    
    # 顯示比較表格
    print(f"\n{'策略':<9} {'期中':>5} {'期末':>5} {'知識':>5} {'GPA':>6} {'標準差':>5}")
    print("-" * 70)
    for name, stats in results.items():
        print(f"{name:<12} {stats['midterm']:7.2f} {stats['final']:7.2f} "
              f"{stats['knowledge']:7.2f} {stats['gpa']:7.2f} {stats['gpa_std']:7.2f}")
    
    # 找出最佳策略
    best_gpa = max(results.items(), key=lambda x: x[1]['gpa'])
    best_knowledge = max(results.items(), key=lambda x: x[1]['knowledge'])
    most_stable = min(results.items(), key=lambda x: x[1]['gpa_std'])
    
    print(f"\n🏆 最高平均 GPA: {best_gpa[0]} ({best_gpa[1]['gpa']:.2f})")
    print(f"📚 最高知識值: {best_knowledge[0]} ({best_knowledge[1]['knowledge']:.2f})")
    print(f"📈 最穩定策略: {most_stable[0]} (標準差 {most_stable[1]['gpa_std']:.2f})")
    
    # 策略特點說明
    print(f"\n💡 策略特點分析:")
    print(f"   保守平衡型: 各項屬性均衡，心情體力最好，但成績較低")
    print(f"   激進極端型: 知識最高，可能達到滿分，但心情體力會很差")
    print(f"   隨性自由型: 變化最大，享受過程，成績中等")
    print(f"   有限狀態機: 動態調整，平衡成績與身心狀態，最推薦")
    
    return results


def compare_policies_by_character(n_players: int = 300):
    """針對四種角色分別測試三種個性策略，並輸出圖表與統計。"""
    print(f"\n{'='*70}")
    print(f"  🧪 角色 × 個性 策略對照（每組 {n_players} 名玩家）")
    print(f"{'='*70}\n")

    characters = [Bubu, Yier, Mitao, Huihui]
    policies = {
        "Conservative": ConservativePolicy(epsilon=0.1),
        "Aggressive": AggressivePolicy(epsilon=0.05),
        "Casual": CasualPolicy(epsilon=0.4),
    }

    # 結果收集：{character: {policy: stats}}
    all_results: dict[str, dict[str, dict]] = {}

    for char_cls in characters:
        char_name = char_cls.__name__
        print(f"🔹 角色：{char_name}")
        all_results[char_name] = {}

        for policy_name, policy in policies.items():
            print(f"  └─ 模擬 {policy_name}... ", end='', flush=True)
            out_dir = f"simulation_plots/{char_name}_run/{policy_name.replace(' ', '')}_policy"

            sim = Simulation(
                n_players=n_players,
                policy=policy,
                characters=[char_cls],
                out_dir=out_dir,
            )

            sim.run()
            sim.plot_midterm_final(title_add=f" ({char_name} - {policy_name})")
            sim.plot_total(title_add=f" ({char_name} - {policy_name})")
            sim.plot_gpa(title_add=f" ({char_name} - {policy_name})")
            sim.export_gpa_csv()
            print("✓")

            stats = {
                'midterm': statistics.mean(sim.midterm),
                'final': statistics.mean(sim.final),
                'knowledge': statistics.mean(sim.knowledge),
                'gpa': statistics.mean(sim.gpa),
                'gpa_std': statistics.stdev(sim.gpa) if len(sim.gpa) > 1 else 0,
            }
            all_results[char_name][policy_name] = stats

        # 角色總結表格
        print(f"\n  📈 {char_name} 總結：")
        print(f"    {'策略':<9} {'期中':>5} {'期末':>5} {'知識':>6} {'GPA':>6} {'標準差':>7}")
        print("    " + "-" * 60)
        for policy_name, stats in all_results[char_name].items():
            print(
                f"    {policy_name:<14} {stats['midterm']:7.2f} {stats['final']:7.2f} "
                f"{stats['knowledge']:7.2f} {stats['gpa']:7.2f} {stats['gpa_std']:7.2f}"
            )

        # 找出該角色的最佳策略
        best_gpa = max(all_results[char_name].items(), key=lambda x: x[1]['gpa'])
        best_knowledge = max(all_results[char_name].items(), key=lambda x: x[1]['knowledge'])
        most_stable = min(all_results[char_name].items(), key=lambda x: x[1]['gpa_std'])

        print(
            f"\n  🏆 {char_name} — 最高 GPA: {best_gpa[0]} ({best_gpa[1]['gpa']:.2f}) | "
            f"最高知識: {best_knowledge[0]} ({best_knowledge[1]['knowledge']:.2f}) | "
            f"最穩定: {most_stable[0]} (Std {most_stable[1]['gpa_std']:.2f})\n"
        )

    print(f"{'='*70}\n")
    print("所有輸出已保存到 simulation_plots/{角色}_run/{策略}_policy 目錄")
    return all_results

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🎓 AI 行為樹策略測試系統  ".center(70))
    print("="*70)
    
    print("\n本測試將展示四種不同的決策策略：")
    print("  1️⃣  保守平衡型 - 維持各項數值均衡")
    print("  2️⃣  激進極端型 - 追求極致，可能專注單一行為")
    print("  3️⃣  隨性自由型 - 高隨機性，跟隨心情做決定")
    print("  4️⃣  有限狀態機 - 在上述三種策略間動態切換")
    
    # 1. 測試保守型策略
    conservative_result = test_single_policy(
        ConservativePolicy(epsilon=0.1), 
        "保守平衡型"
    )
    
    # 2. 測試激進型策略
    aggressive_result = test_single_policy(
        AggressivePolicy(epsilon=0.05), 
        "激進極端型"
    )
    
    # 3. 測試隨性型策略
    casual_result = test_single_policy(
        CasualPolicy(epsilon=0.4), 
        "隨性自由型"
    )
    
    # 4. 測試 FSM 策略（含詳細追蹤）
    fsm_result = test_fsm_policy_with_details()
    
    # 5. 比較所有策略
    all_results = compare_all_policies()

    # 6. 角色 × 個性 三向測試
    compare_policies_by_character(n_players=300)
    
    print(f"\n{'='*70}")
    print("  ✅ 測試完成！".center(70))
    print(f"{'='*70}")
    print(f"\n所有圖表已儲存至 simulation_plots/ 目錄下")
    print(f"可查看各策略的期中/期末/GPA 分佈圖\n")
