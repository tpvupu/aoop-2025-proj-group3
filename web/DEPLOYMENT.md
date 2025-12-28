# 部署到 GitHub Pages

## 步驟一：準備 Repository

1. 登入 GitHub
2. 創建新的 repository：`lazy-me-today-too-web`
3. 設為 Public（GitHub Pages 免費版需要）

## 步驟二：上傳文件

### 方法 A：使用 Git 命令

```bash
cd web
git init
git add .
git commit -m "Initial commit: Web version of Lazy Me Today Too"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/lazy-me-today-too-web.git
git push -u origin main
```

### 方法 B：直接拖放上傳

1. 在 GitHub repository 頁面點擊 "uploading an existing file"
2. 將 `web` 目錄下的所有文件拖放到頁面
3. 提交變更

## 步驟三：啟用 GitHub Pages

1. 進入 repository 的 **Settings**
2. 左側選單找到 **Pages**
3. 在 "Source" 部分：
   - Branch 選擇：`main`
   - Folder 選擇：`/ (root)`
4. 點擊 **Save**
5. 等待幾分鐘，會顯示網址：
   ```
   https://YOUR_USERNAME.github.io/lazy-me-today-too-web/
   ```

## 步驟四：驗證部署

訪問生成的網址，確認遊戲正常運行。

---

# 部署到 Netlify

## 方法一：拖放部署（最簡單）

1. 訪問 [Netlify](https://www.netlify.com/)
2. 註冊或登入帳號
3. 點擊 "Add new site" → "Deploy manually"
4. 將整個 `web` 目錄拖放到頁面
5. 等待部署完成
6. 獲得網址：`https://random-name.netlify.app`

## 方法二：連接 Git Repository

1. 將代碼推送到 GitHub
2. 在 Netlify 選擇 "Import from Git"
3. 連接 GitHub 帳號
4. 選擇 repository
5. 設定：
   - Base directory: `web`
   - Build command: （留空）
   - Publish directory: `.`
6. 點擊 "Deploy"

## 自定義域名（可選）

在 Netlify 的 Domain Settings 中：
1. 點擊 "Add custom domain"
2. 輸入你的域名
3. 按照指示設定 DNS 記錄

---

# 部署到 Vercel

1. 訪問 [Vercel](https://vercel.com/)
2. 使用 GitHub 登入
3. 點擊 "New Project"
4. 選擇你的 repository
5. 設定：
   - Root Directory: `web`
   - Framework Preset: Other
6. 點擊 "Deploy"

---

# 部署到 Firebase Hosting

## 步驟一：安裝 Firebase CLI

```bash
npm install -g firebase-tools
```

## 步驟二：初始化項目

```bash
cd web
firebase login
firebase init hosting
```

選擇：
- What do you want to use as your public directory? (public) **.**
- Configure as a single-page app? **Y**
- Set up automatic builds and deploys with GitHub? **N**

## 步驟三：部署

```bash
firebase deploy
```

獲得網址：`https://your-project.web.app`

---

# 本地測試

在部署前，務必本地測試：

```bash
cd web
python3 -m http.server 8000
# 或
./start.sh
```

訪問 `http://localhost:8000` 確認一切正常。

---

# 故障排除

## 問題：頁面空白

**原因**：路徑錯誤或 CORS 問題

**解決**：
1. 檢查瀏覽器控制台（F12）的錯誤訊息
2. 確認所有資源路徑正確
3. 使用 HTTP 伺服器運行，不要直接打開 HTML

## 問題：Phaser 無法載入

**原因**：CDN 連接失敗

**解決**：
1. 檢查網路連接
2. 下載 Phaser.js 到本地：
   ```bash
   cd web
   mkdir lib
   wget https://cdn.jsdelivr.net/npm/phaser@3.70.0/dist/phaser.min.js -O lib/phaser.min.js
   ```
3. 修改 index.html：
   ```html
   <script src="lib/phaser.min.js"></script>
   ```

## 問題：圖片/音效無法載入

**原因**：資源路徑錯誤

**解決**：
1. 確認資源文件已上傳
2. 檢查路徑大小寫（Linux 區分大小寫）
3. 使用相對路徑而非絕對路徑

---

# 效能優化建議

## 1. 壓縮資源

```bash
# 壓縮圖片
find . -name "*.png" -exec pngquant --force --ext .png {} \;

# 壓縮 JavaScript
npx terser js/main.js -o js/main.min.js
```

## 2. 使用 CDN

已使用 jsDelivr CDN 載入 Phaser，無需額外操作。

## 3. 啟用快取

在部署平台設定 HTTP 快取頭：

```
Cache-Control: public, max-age=31536000
```

## 4. 使用 Service Worker

創建 `sw.js` 實現離線快取（進階）。

---

**選擇最適合你的部署方式，開始分享你的遊戲吧！🚀**
