#!/bin/bash

# 打包腳本 - 用於將專案打包成可執行文件

echo "======================================"
echo "開始打包 Lazy Me Today Too"
echo "======================================"

# 1. 安裝 PyInstaller（如果尚未安裝）
echo "檢查 PyInstaller..."
if ! pip show pyinstaller &> /dev/null; then
    echo "安裝 PyInstaller..."
    pip install pyinstaller
else
    echo "PyInstaller 已安裝"
fi

# 2. 清理之前的打包文件
echo "清理舊的打包文件..."
rm -rf build dist

# 3. 執行打包
echo "開始打包..."
pyinstaller build.spec

# 4. 檢查結果
if [ -d "dist/LazyMeTodayToo.app" ]; then
    echo "======================================"
    echo "打包成功！"
    echo "應用程式位置: dist/LazyMeTodayToo.app"
    echo "======================================"
    echo ""
    echo "使用方式："
    echo "1. 在 Finder 中打開 dist 資料夾"
    echo "2. 雙擊 LazyMeTodayToo.app 即可執行"
    echo ""
    echo "如需發布，可以將 dist/LazyMeTodayToo.app 複製到其他 Mac 電腦使用"
else
    echo "======================================"
    echo "打包失敗，請檢查錯誤訊息"
    echo "======================================"
fi
