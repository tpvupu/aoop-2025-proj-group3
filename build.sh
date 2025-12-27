#!/bin/bash

# 打包腳本 - 用於將專案打包成可執行文件

echo "======================================"
echo "開始打包 Lazy Me Today Too"
echo "======================================"

# 1. 安裝 PyInstaller 和必要依賴（如果尚未安裝）
echo "檢查打包依賴..."
if ! pip show pyinstaller &> /dev/null; then
    echo "安裝 PyInstaller..."
    pip install pyinstaller
else
    echo "PyInstaller 已安裝"
fi

# OpenAI API 需要的 SSL/HTTP 依賴
echo "檢查 SSL/HTTP 依賴..."
pip install certifi httpx -q

# 2. 準備應用程式圖示（由 PNG 轉成 macOS .icns）
ICON_SRC="resource/image/Mitao_head.png"
ICON_ICNS="resource/image/Mitao_head.icns"

echo "準備應用程式圖示..."
if [ -f "$ICON_SRC" ]; then
    if command -v iconutil >/dev/null 2>&1 && command -v sips >/dev/null 2>&1; then
        if [ ! -f "$ICON_ICNS" ] || [ "$ICON_SRC" -nt "$ICON_ICNS" ]; then
            echo "生成 macOS .icns 圖示..."
            ICONSET_DIR="$(mktemp -d)"
            mkdir -p "$ICONSET_DIR"
            for size in 16 32 64 128 256 512 1024; do
                sips -z $size $size "$ICON_SRC" --out "$ICONSET_DIR/icon_${size}x${size}.png" >/dev/null
            done
            iconutil -c icns "$ICONSET_DIR" -o "$ICON_ICNS" >/dev/null
            rm -rf "$ICONSET_DIR"
        else
            echo "已存在最新的 .icns，跳過生成"
        fi
    else
        echo "未找到 iconutil 或 sips，跳過圖示轉換，將使用預設圖示"
    fi
else
    echo "找不到圖示來源 $ICON_SRC，將使用預設圖示"
fi

# 3. 清理之前的打包文件
echo "清理舊的打包文件..."
rm -rf build dist

# 4. 執行打包
echo "開始打包..."
pyinstaller build.spec

# 5. 檢查結果
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
