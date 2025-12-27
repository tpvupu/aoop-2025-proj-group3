# 專案打包指南

## 快速開始

### 在 macOS 上打包（生成 .app 文件）

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **執行打包**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

3. **運行應用程式**
   - 打包完成後，在 `dist/` 資料夾中會生成 `LazyMeTodayToo.app`
   - 雙擊即可執行

---

## 在 Windows 上打包（生成 .exe 文件）

如果您需要 Windows 版本的 exe 文件，需要在 Windows 環境中執行：

### 方法一：使用 Windows 電腦

1. **安裝 Python 和依賴**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **修改 build.spec**
   - 移除或註解掉最後的 `BUNDLE` 部分（僅用於 macOS）
   - 確保 `console=False` 以隱藏命令提示字元視窗

3. **執行打包**
   ```cmd
   pyinstaller build.spec
   ```

4. **結果**
   - 在 `dist/LazyMeTodayToo/` 資料夾中會有可執行文件
   - 整個資料夾都需要一起發布

### 方法二：使用單一 exe 文件

如果想要打包成單一 exe 文件（較慢但更方便發布）：

```bash
pyinstaller --onefile --windowed \
  --add-data "resource:resource" \
  --add-data "event/events.json:event" \
  --add-data "AI:AI" \
  --name LazyMeTodayToo \
  main.py
```

---

## 常見問題

### Q1: 打包後無法找到資源文件
**A:** 確保所有資源文件都在 `build.spec` 的 `datas` 列表中

### Q2: 打包檔案太大
**A:** 
- 使用虛擬環境，只安裝必要的套件
- 考慮移除不必要的依賴（如 pytest）

### Q3: macOS 提示「無法打開應用程式，因為它來自未識別的開發者」
**A:** 
```bash
# 臨時允許執行
xattr -cr dist/LazyMeTodayToo.app

# 或在系統偏好設定 > 安全性與隱私權中允許
```

### Q4: 程式執行時出現錯誤
**A:** 
- 暫時設置 `console=True` 查看錯誤訊息
- 檢查所有資源路徑是否正確

---

## 進階設定

### 添加圖示

1. 準備圖示文件：
   - macOS: `.icns` 格式
   - Windows: `.ico` 格式

2. 修改 `build.spec`：
   ```python
   exe = EXE(
       ...
       icon='path/to/icon.icns',  # macOS
       # icon='path/to/icon.ico',  # Windows
       ...
   )
   ```

### 優化打包大小

1. 使用虛擬環境
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS
   pip install -r requirements.txt
   ```

2. 排除不需要的模組
   在 `build.spec` 的 `excludes` 中添加：
   ```python
   excludes=['pytest', 'test', 'pygbag'],
   ```

### 跨平台打包建議

- 無法在 macOS 上直接生成 Windows exe
- 無法在 Windows 上直接生成 macOS app
- 建議使用 CI/CD 或虛擬機進行跨平台打包

---

## 檔案說明

- `build.spec`: PyInstaller 配置文件
- `build.sh`: macOS 打包腳本
- `dist/`: 打包輸出目錄
- `build/`: 臨時構建文件（可刪除）

---

## 發布檢查清單

- [ ] 測試打包後的應用程式是否能正常運行
- [ ] 檢查所有資源文件是否正確載入
- [ ] 測試音效、圖片、字體是否正常顯示
- [ ] 在乾淨的系統上測試（無 Python 環境）
- [ ] 準備 README 給使用者
