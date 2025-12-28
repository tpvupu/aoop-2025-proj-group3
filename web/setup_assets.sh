#!/bin/bash

# 創建資源目錄結構
echo "🎨 創建資源目錄..."

mkdir -p assets/images
mkdir -p assets/sounds
mkdir -p assets/fonts

echo "✅ 目錄創建完成"
echo ""
echo "📁 資源目錄結構："
echo "web/"
echo "  └── assets/"
echo "      ├── images/     # 放置圖片資源"
echo "      ├── sounds/     # 放置音效資源"
echo "      └── fonts/      # 放置字體資源"
echo ""
echo "💡 下一步："
echo "1. 將原項目的圖片複製到 assets/images/"
echo "2. 將原項目的音效複製到 assets/sounds/"
echo "3. 更新 PreloadScene.js 載入路徑"
echo ""
echo "完成！🎉"
