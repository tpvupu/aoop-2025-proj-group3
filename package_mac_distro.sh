#!/bin/bash
# 嚴格模式：避免未定義變數造成中斷，改用安全展開
set -e -o pipefail

APP_PATH="dist/LazyMeTodayToo.app"
DIST_DIR="dist"
ZIP_NAME="LazyMeTodayToo-mac.zip"
DMG_NAME="LazyMeTodayToo.dmg"
VOL_NAME="LazyMeTodayToo"
MAKE_DMG=false

usage() {
  echo "Usage: $0 [--dmg]"
  echo "  --dmg   同時輸出 DMG 安裝檔"
}

for arg in "$@"; do
  case "$arg" in
    --dmg)
      MAKE_DMG=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      ;;
  esac
done

if [ ! -d "$APP_PATH" ]; then
  echo "找不到 $APP_PATH，請先執行 ./build.sh 進行打包" >&2
  exit 1
fi

mkdir -p "$DIST_DIR"

# 準備 README 與 .env.example
README_FILE="$DIST_DIR/README.txt"
ENV_EXAMPLE="$DIST_DIR/.env.example"

cat > "$README_FILE" << 'EOF'
Lazy Me Today Too 使用說明（macOS）

1) 開啟方式：
   - 在 Finder 中前往此資料夾，右鍵（或按住 control）點擊 LazyMeTodayToo.app，選「打開」，
     再次彈出警告時按「打開」。這是因為未簽名開發者的 Gatekeeper 限制。
   - 若仍被阻擋，可在終端機執行：
       xattr -cr LazyMeTodayToo.app

2) OpenAI API（選用）：
   - 若要使用 AI 建議功能，請將 .env.example 複製為 .env，並填入您的 API Key：
       OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
   - .env 檔案要與 LazyMeTodayToo.app 放在同一層資料夾。

3) 常見問題：
   - 若顯示「來自未識別的開發者」，請用右鍵→打開流程，或在系統設定→隱私與安全性允許。
   - 若 AI 無法連線，請確認網路可連到 https://api.openai.com 並檢查 API Key 是否有效。

祝遊玩愉快！
EOF

# 複製 .env.example（若根目錄已有則優先使用）
if [ -f ".env.example" ]; then
  cp -f ".env.example" "$ENV_EXAMPLE"
else
  echo "OPENAI_API_KEY=your_api_key_here" > "$ENV_EXAMPLE"
fi

# 產出 zip
pushd "$DIST_DIR" >/dev/null
rm -f "$ZIP_NAME"
zip -r "$ZIP_NAME" "$(basename "$APP_PATH")" "$(basename "$README_FILE")" "$(basename "$ENV_EXAMPLE")" >/dev/null
popd >/dev/null

echo "✅ 已生成：${DIST_DIR}/${ZIP_NAME}"

echo "  包含："
echo "    - $(basename "$APP_PATH")"
echo "    - README.txt"
echo "    - .env.example"

# 可選：生成 DMG
if [ "$MAKE_DMG" = true ]; then
  TMP_DIR="$(mktemp -d)"
  cp -R "$APP_PATH" "$TMP_DIR/"
  cp "$README_FILE" "$TMP_DIR/"
  cp "$ENV_EXAMPLE" "$TMP_DIR/"
  hdiutil create -volname "$VOL_NAME" -srcfolder "$TMP_DIR" -ov "$DIST_DIR/$DMG_NAME" >/dev/null
  rm -rf "$TMP_DIR"
  echo "✅ 已生成：$DIST_DIR/$DMG_NAME"
fi

echo "完成！您可將 ${DIST_DIR}/${ZIP_NAME}（或 DMG）直接分享給其他 mac 使用者。" 
