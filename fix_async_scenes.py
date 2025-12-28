#!/usr/bin/env python3
"""
批量修復所有場景的 async run() 方法
"""
import re
import os

scenes_to_fix = [
    'UI/main_scene.py',
    'UI/event_scene.py',
    'UI/story_scene.py',
    'UI/end_scene.py',
    'UI/rank_scene.py',
    'UI/diary_scene.py',
    'UI/feedback_scene.py',
    'UI/advice_scene.py',
    'UI/sound_control_scene.py',
    'UI/set_scene.py',
    'UI/taketest_scene.py',
    'UI/lucky_wheel_scene.py',
    'UI/confirm_reborn_scene.py',
]

def fix_scene(filepath):
    if not os.path.exists(filepath):
        print(f"⏭️  Skipping {filepath} (not found)")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # 添加 asyncio import (如果還沒有)
    if 'import asyncio' not in content:
        # 在第一個 import 後添加
        content = re.sub(
            r'(import .*?\n)',
            r'\1import asyncio\n',
            content,
            count=1
        )
        modified = True
    
    # 修改 def run(self): 為 async def run(self):
    if re.search(r'\n    def run\(self\):', content):
        content = re.sub(
            r'\n    def run\(self\):',
            r'\n    async def run(self):',
            content
        )
        modified = True
    
    # 在 while 循環開始後添加 await asyncio.sleep(0)
    # 模式: while self.running: 後面沒有 await asyncio.sleep(0)
    pattern = r'(while self\.running:)\n(\s+)(?!await asyncio\.sleep)'
    if re.search(pattern, content):
        content = re.sub(
            pattern,
            r'\1\n\2await asyncio.sleep(0)\n\2',
            content
        )
        modified = True
    
    # 另一個常見模式: while running:
    pattern = r'(while running:)\n(\s+)(?!await asyncio\.sleep)'
    if re.search(pattern, content):
        content = re.sub(
            pattern,
            r'\1\n\2await asyncio.sleep(0)\n\2',
            content
        )
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {filepath}")
        return True
    else:
        print(f"✓  {filepath} already correct")
        return False

if __name__ == '__main__':
    print("🔧 Fixing async run() methods in all scenes...")
    print("=" * 50)
    
    fixed_count = 0
    for scene in scenes_to_fix:
        if fix_scene(scene):
            fixed_count += 1
    
    print("=" * 50)
    print(f"✅ Fixed {fixed_count} files")
    print("\nRun 'python3 test_web_compatibility.py' to verify!")
