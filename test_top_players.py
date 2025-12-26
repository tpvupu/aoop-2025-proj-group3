#!/usr/bin/env python3
# test_top_players.py
"""測試腳本：顯示 GPA 最高的前幾名玩家資訊"""

import sys
import os

# 確保可以導入專案模組
sys.path.insert(0, os.path.dirname(__file__))

from simulation import Simulation
from bvtree import *

if __name__ == "__main__":
    print("開始執行模擬...")
    policy = FSMBehaviorPolicy()
    sim = Simulation(n_players=300, policy=policy)
    sim.run()
    print("模擬完成！\n")
    
    # 分別顯示每個角色的前 3 名
    sim.show_top_players_by_character(top_n=3)
    
    # 如果想看全體排名前 10 名，取消下面這行註解
    # sim.show_top_players(top_n=10)
