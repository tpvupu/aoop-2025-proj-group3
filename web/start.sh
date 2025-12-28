#!/bin/bash

# 網頁版快速啟動腳本
# Quick start script for web version

echo "🎮 今天的我也想耍廢 - 網頁版啟動器"
echo "================================"
echo ""

# 檢查是否在 web 目錄
if [ ! -f "index.html" ]; then
    echo "❌ 錯誤：請在 web 目錄下運行此腳本"
    echo "請執行：cd web && ./start.sh"
    exit 1
fi

# 檢測可用的 HTTP 伺服器
if command -v python3 &> /dev/null; then
    echo "✅ 使用 Python 3 啟動伺服器..."
    echo "🌐 遊戲將在 http://localhost:8000 運行"
    echo "📝 按 Ctrl+C 停止伺服器"
    echo ""
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "✅ 使用 Python 2 啟動伺服器..."
    echo "🌐 遊戲將在 http://localhost:8000 運行"
    echo "📝 按 Ctrl+C 停止伺服器"
    echo ""
    python -m SimpleHTTPServer 8000
elif command -v npx &> /dev/null; then
    echo "✅ 使用 Node.js http-server 啟動伺服器..."
    echo "🌐 遊戲將在 http://localhost:8000 運行"
    echo "📝 按 Ctrl+C 停止伺服器"
    echo ""
    npx http-server -p 8000
else
    echo "❌ 未找到可用的 HTTP 伺服器"
    echo ""
    echo "請安裝以下任一工具："
    echo "  - Python 3: https://www.python.org/"
    echo "  - Node.js: https://nodejs.org/"
    echo ""
    echo "或使用 VS Code 的 Live Server 擴充套件"
    exit 1
fi
