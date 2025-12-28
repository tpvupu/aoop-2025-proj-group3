# 🎮 Web 版本部署檢查清單

## ✅ 已完成的修改

### 1. 代碼修改
- [x] 將 `main.py` 改為使用 `asyncio.run()`
- [x] 將 `SceneManager.run()` 改為 async 函數
- [x] 將所有場景方法改為 async 函數
- [x] 將 `BaseScene.run()` 改為 async 函數
- [x] 在主循環中添加 `await asyncio.sleep(0)`

### 2. 配置文件
- [x] 創建 `index.html` - Web 遊戲入口
- [x] 創建 `.pygbagrc` - Pygbag 配置
- [x] 創建 `build_web.sh` - 構建腳本
- [x] 創建 `.github/workflows/deploy.yml` - GitHub Actions 自動部署
- [x] 更新 `.gitignore` - 排除 web 構建文件
- [x] 更新 `README.md` - 添加 Web 版本說明

### 3. 測試
- [x] 創建 `test_web_compatibility.py` - 兼容性測試
- [x] 運行測試確認所有修改正確

## 📋 部署前檢查

在推送到 GitHub 之前，請確認：

### 必要檢查
- [ ] 所有測試通過 (`python3 test_web_compatibility.py`)
- [ ] 本地桌面版仍能正常運行 (`python3 main.py`)
- [ ] 所有資源文件已提交到 Git
- [ ] requirements.txt 包含 pygbag

### 可選檢查
- [ ] 已壓縮大型圖片資源
- [ ] 已測試本地 Web 版本 (`./build_web.sh`)
- [ ] OpenAI API 功能已處理（Web 版本可能不支援）

## 🚀 部署步驟

### 方法 1: 自動部署（推薦）

1. **提交並推送代碼**
   ```bash
   git add .
   git commit -m "Add web deployment support"
   git push origin main
   ```

2. **啟用 GitHub Pages**
   - 進入倉庫 Settings → Pages
   - Source 選擇 "GitHub Actions"

3. **等待部署完成**
   - 檢查 Actions 標籤
   - 約 3-5 分鐘後完成
   - 訪問 `https://<username>.github.io/<repo-name>/`

### 方法 2: 本地構建測試

1. **構建 Web 版本**
   ```bash
   ./build_web.sh
   ```

2. **本地測試**
   ```bash
   python3 -m http.server --directory build/web 8000
   # 打開 http://localhost:8000
   ```

3. **確認功能正常後再推送**

## ⚠️ 注意事項

### Web 版本限制
- OpenAI API 功能不可用（需要後端支援）
- 首次載入較慢（需下載所有資源，約 50-100MB）
- 某些瀏覽器可能需要用戶互動才能播放音效

### 相容性
- 建議瀏覽器：Chrome 90+, Firefox 88+, Safari 14+
- 需要 WebAssembly 支援
- 需要 WebGL 支援（用於 Pygame）

### 性能優化建議
- 降低 FPS 到 30（在 base_scene.py）
- 壓縮圖片資源
- 減少 GIF 動畫幀數
- 使用 CDN（在 .pygbagrc 中啟用）

## 📝 更新 README

別忘記更新 README.md 中的連結：

```markdown
🎮 **[立即在線遊玩（Web版）](https://YOUR_USERNAME.github.io/aoop-2025-proj-group3/)**
```

將 `YOUR_USERNAME` 替換為你的 GitHub 用戶名。

## 🔧 故障排除

### 部署失敗
1. 檢查 GitHub Actions 日誌
2. 確認 Python 版本（3.11+）
3. 確認所有依賴都在 requirements.txt

### 遊戲無法載入
1. 檢查瀏覽器控制台（F12）
2. 清除瀏覽器緩存（Ctrl+Shift+R）
3. 確認所有資源文件存在

### 性能問題
1. 降低 FPS
2. 壓縮資源
3. 使用較小的視窗大小

## 📚 相關文檔

- [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) - 詳細部署指南
- [README.md](README.md) - 專案說明
- [Pygbag 文檔](https://pygame-web.github.io/)

## ✨ 完成！

當你完成上述所有步驟後，你的遊戲就可以在網頁上運行了！

分享你的遊戲連結：
```
https://<username>.github.io/aoop-2025-proj-group3/
```

祝你部署順利！🎉
