# 貢獻指南

感謝你考慮為 Project Observer 做出貢獻！

## 如何貢獻

### 報告 Bug

如果你發現 Bug，請創建一個 Issue 並包含：

- 問題的清晰描述
- 復現步驟
- 預期行為 vs 實際行為
- 環境信息（OS、Docker 版本等）
- 相關日誌

### 建議新功能

我們歡迎新功能建議！請創建 Issue 並說明：

- 功能的用途和價值
- 預期的使用場景
- 可能的實現方案

### 提交代碼

1. **Fork 專案**
   ```bash
   # 在 GitHub 上點擊 Fork
   git clone https://github.com/YOUR_USERNAME/Project-Observer.git
   cd Project-Observer
   ```

2. **創建分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **進行修改**
   - 遵循現有的代碼風格
   - 添加必要的註釋
   - 更新相關文檔

4. **測試**
   ```bash
   # 確保系統能正常啟動
   make start
   
   # 驗證功能
   make logs-ai
   ```

5. **提交變更**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

6. **推送到 GitHub**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **創建 Pull Request**
   - 在 GitHub 上打開 Pull Request
   - 清楚描述你的變更
   - 關聯相關的 Issue

## 代碼規範

### Python 代碼

```python
# 使用 PEP 8 風格
# 使用類型提示
def function_name(param: str) -> Dict[str, Any]:
    """
    函數說明
    
    Args:
        param: 參數說明
        
    Returns:
        返回值說明
    """
    pass
```

### JavaScript 代碼

```javascript
// 使用 async/await
// 添加清晰的註釋
async function functionName(param) {
    // 實現
}
```

### Commit 訊息

使用語義化提交訊息：

- `feat:` 新功能
- `fix:` Bug 修復
- `docs:` 文檔更新
- `style:` 代碼格式
- `refactor:` 重構
- `test:` 測試
- `chore:` 構建/工具變更

例如：
```
feat: add skill priority system
fix: resolve memory leak in bot controller
docs: update installation guide
```

## 開發環境設置

```bash
# 1. Clone 並進入目錄
git clone https://github.com/YOUR_USERNAME/Project-Observer.git
cd Project-Observer

# 2. 創建 .env
cp .env.example .env
# 填入你的 API Key

# 3. 啟動開發環境
make start

# 4. 查看日誌
make logs-ai
```

## 測試指南

### 手動測試

1. 啟動系統並觀察 AI 行為
2. 檢查 Dashboard 是否正常顯示
3. 嘗試加入 Minecraft 服務器
4. 驗證技能保存和讀取

### 日誌檢查

```bash
# 確保沒有錯誤
make logs-ai | grep ERROR

# 確認 AI 循環正常
make logs-ai | grep "Iteration"
```

## 需要幫助的領域

我們特別歡迎以下方面的貢獻：

- 🧠 **AI 策略優化**：改進決策算法
- 🎮 **更多技能**：添加預設技能模板
- 📊 **Dashboard 增強**：更多可視化功能
- 🔧 **性能優化**：減少資源消耗
- 📚 **文檔完善**：教程、示例
- 🌍 **多語言支持**：翻譯文檔和界面

## 問題與討論

- 💬 [Discussions](https://github.com/RainesTaiwan/Project-Observer/discussions) - 提問和討論
- 🐛 [Issues](https://github.com/RainesTaiwan/Project-Observer/issues) - Bug 報告和功能請求

## 行為準則

- 尊重所有貢獻者
- 保持建設性的討論
- 接受建設性的批評
- 關注對社區最有利的事情

## 聯繫

如有任何問題，請聯繫：
- GitHub: [@RainesTaiwan](https://github.com/RainesTaiwan)

---

再次感謝你的貢獻！🎉
