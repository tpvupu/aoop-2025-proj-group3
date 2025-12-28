#!/usr/bin/env python3
"""
測試腳本 - 驗證 Web 版本的 asyncio 兼容性
"""

import asyncio
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_import():
    """測試所有模組是否能正確導入"""
    print("🔍 測試模組導入...")
    
    try:
        from scene_manager import SceneManager
        print("✅ scene_manager 導入成功")
    except Exception as e:
        print(f"❌ scene_manager 導入失敗: {e}")
        return False
    
    try:
        from UI.components.base_scene import BaseScene
        print("✅ base_scene 導入成功")
    except Exception as e:
        print(f"❌ base_scene 導入失敗: {e}")
        return False
    
    try:
        import character
        print("✅ character 導入成功")
    except Exception as e:
        print(f"❌ character 導入失敗: {e}")
        return False
    
    print("\n✅ 所有模組導入成功！")
    return True

async def test_asyncio_structure():
    """測試 asyncio 結構是否正確"""
    print("\n🔍 測試 asyncio 結構...")
    
    try:
        from scene_manager import SceneManager
        import inspect
        
        # 檢查 SceneManager.run 是否為 async
        if inspect.iscoroutinefunction(SceneManager.run):
            print("✅ SceneManager.run 是異步函數")
        else:
            print("❌ SceneManager.run 不是異步函數")
            return False
        
        # 檢查場景方法是否為 async
        scene_methods = [
            'first_scene', 'start_scene', 'character_select', 
            'main_game_loop', 'story_and_event'
        ]
        
        for method_name in scene_methods:
            method = getattr(SceneManager, method_name, None)
            if method and inspect.iscoroutinefunction(method):
                print(f"✅ SceneManager.{method_name} 是異步函數")
            else:
                print(f"❌ SceneManager.{method_name} 不是異步函數")
                return False
        
        print("\n✅ asyncio 結構正確！")
        return True
        
    except Exception as e:
        print(f"❌ asyncio 結構測試失敗: {e}")
        return False

async def test_base_scene():
    """測試 BaseScene 的 async 兼容性"""
    print("\n🔍 測試 BaseScene...")
    
    try:
        from UI.components.base_scene import BaseScene
        import inspect
        
        if inspect.iscoroutinefunction(BaseScene.run):
            print("✅ BaseScene.run 是異步函數")
        else:
            print("❌ BaseScene.run 不是異步函數")
            return False
        
        print("✅ BaseScene 測試通過！")
        return True
        
    except Exception as e:
        print(f"❌ BaseScene 測試失敗: {e}")
        return False

async def main():
    """主測試函數"""
    print("=" * 50)
    print("🎮 Lazy Me Today Too - Web 版本測試")
    print("=" * 50)
    print()
    
    results = []
    
    # 運行測試
    results.append(await test_import())
    results.append(await test_asyncio_structure())
    results.append(await test_base_scene())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 所有測試通過！遊戲已準備好進行 Web 部署。")
        print("=" * 50)
        print("\n下一步：")
        print("1. 運行 ./build_web.sh 構建 Web 版本")
        print("2. 推送代碼到 GitHub")
        print("3. 啟用 GitHub Pages")
        return 0
    else:
        print("❌ 部分測試失敗。請檢查上述錯誤訊息。")
        print("=" * 50)
        return 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
