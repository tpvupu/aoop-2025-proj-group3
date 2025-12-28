# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

is_macos = sys.platform == "darwin"
is_windows = sys.platform.startswith("win")

icon_path = None
if is_macos and os.path.exists("resource/image/Mitao_head.icns"):
    icon_path = "resource/image/Mitao_head.icns"
elif is_windows and os.path.exists("resource/image/Mitao_head.ico"):
    icon_path = "resource/image/Mitao_head.ico"

# 收集 certifi 的 SSL 證書（OpenAI API 需要）
try:
    import certifi
    cert_datas = [(certifi.where(), 'certifi')]
except ImportError:
    cert_datas = []

# 收集 openai 相關模組
openai_hiddenimports = collect_submodules('openai')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resource', 'resource'),
        ('event/events.json', 'event'),
        ('AI', 'AI'),
    ] + cert_datas + collect_data_files('certifi'),
    hiddenimports=[
        'pygame',
        'numpy',
        'pandas',
        'matplotlib',
        'pygame_gui',
        'PIL',
        'openai',
        'openai.types',
        'openai.resources',
        'httpx',
        'certifi',
        'ssl',
        'urllib3',
    ] + openai_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LazyMeTodayToo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 設為 False 隱藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LazyMeTodayToo',
)

if is_macos:
    app = BUNDLE(
        coll,
        name='LazyMeTodayToo.app',
        icon=icon_path,
        bundle_identifier='com.yourcompany.lazyme',
    )
