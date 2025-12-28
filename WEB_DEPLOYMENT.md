# 🚀 Web 版本部署指南

## 概述

本指南將幫助你將 "Lazy Me Today Too" 遊戲部署到 GitHub Pages，讓玩家可以直接在瀏覽器中遊玩。

## 前置需求

- Python 3.11+
- Git
- GitHub 帳號
- pygbag (`pip install pygbag`)

## 快速部署步驟

### 1. 準備代碼

確保你的代碼已經推送到 GitHub：

```bash
git add .
git commit -m "Add web deployment support"
git push origin main
```

### 2. 啟用 GitHub Pages

1. 進入你的 GitHub 倉庫頁面
2. 點擊 **Settings** (設置)
3. 在左側菜單找到 **Pages**
4. 在 "Source" 下選擇 **GitHub Actions**

### 3. 自動部署

一旦你推送代碼到 main/master 分支：
- GitHub Actions 會自動觸發
- 大約 3-5 分鐘後，你的遊戲就會上線
- 訪問 `https://<your-username>.github.io/aoop-2025-proj-group3/`

### 4. 監控部署狀態

1. 在 GitHub 倉庫頁面，點擊 **Actions** 標籤
2. 查看最新的 workflow run
3. 如果看到綠色的 ✓，表示部署成功

## 本地測試 Web 版本

在推送到 GitHub 之前，建議先在本地測試：

```bash
# 1. 構建 web 版本
./build_web.sh

# 2. 啟動本地伺服器
python -m http.server --directory build/web 8000

# 3. 在瀏覽器中打開
# http://localhost:8000
```

## 手動部署（可選）

如果你想手動控制部署過程：

```bash
# 1. 構建遊戲
pygbag --build main.py

# 2. 創建 gh-pages 分支
git checkout -b gh-pages

# 3. 複製構建文件
cp -r build/web/* .

# 4. 提交並推送
git add .
git commit -m "Deploy web version"
git push origin gh-pages

# 5. 回到主分支
git checkout main
```

## 故障排除

### 部署失敗

**檢查 Actions 日誌：**
1. 進入 GitHub Actions
2. 點擊失敗的 workflow
3. 查看詳細錯誤訊息

**常見問題：**
- Python 版本不匹配 → 檢查 `.github/workflows/deploy.yml`
- 資源文件缺失 → 確保所有資源都已提交
- 權限問題 → 確保 Pages 權限已啟用

### 遊戲無法載入

1. **檢查瀏覽器控制台** (F12)
2. **清除瀏覽器緩存** (Ctrl+Shift+R)
3. **確認所有資源文件都存在**

### 音效無法播放

- 某些瀏覽器需要用戶互動後才能播放音頻
- 確保資源文件格式支援（推薦 .ogg, .mp3）

## 優化建議

### 減少載入時間

1. **壓縮圖片資源**
   ```bash
   # 使用 imagemagick 壓縮
   for img in resource/image/**/*.png; do
     convert "$img" -quality 85 "$img"
   done
   ```

2. **減少 GIF 幀數**
   - 降低動畫幀率
   - 使用較小的解析度

3. **使用 CDN**
   - 在 `.pygbagrc` 中啟用 `cdn = true`

### 提升性能

1. **優化 FPS**
   ```python
   # 在 base_scene.py 中調整
   self.FPS = 30  # 降低到 30 FPS 提升性能
   ```

2. **延遲加載資源**
   - 僅在需要時載入大型資源
   - 使用佔位符圖片

## 更新部署

每次修改代碼後：

```bash
git add .
git commit -m "Update game"
git push origin main
```

GitHub Actions 會自動重新部署。

## 自定義域名（可選）

如果你有自己的域名：

1. 在倉庫根目錄創建 `CNAME` 文件
2. 填入你的域名：`game.yourdomain.com`
3. 在域名提供商設置 DNS：
   ```
   Type: CNAME
   Name: game
   Value: <your-username>.github.io
   ```

## 資源

- [Pygbag 官方文檔](https://pygame-web.github.io/)
- [GitHub Pages 文檔](https://docs.github.com/pages)
- [GitHub Actions 文檔](https://docs.github.com/actions)

## 支援

如果遇到問題：
1. 檢查本文件的故障排除部分
2. 查看 GitHub Issues
3. 聯繫開發團隊

---

**祝你部署順利！🎉**
