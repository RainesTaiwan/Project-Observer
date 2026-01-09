# 🌐 GitHub Codespaces 使用指南

在 GitHub Codespaces 環境中使用 Project Observer 的完整指南。

---

## 🚀 快速開始

### 1. 啟動系統

```bash
# 已經完成！系統正在運行
docker-compose ps
```

### 2. 訪問服務

| 服務 | 可用性 | 訪問方式 |
|------|--------|---------|
| **📊 Dashboard** | ✅ 完全可用 | 通過瀏覽器訪問轉發的 8501 端口 |
| **💾 ChromaDB** | ✅ 完全可用 | 通過瀏覽器訪問轉發的 8000 端口 |
| **🎮 Minecraft** | ⚠️ 需要設置 | 需要 TCP 端口轉發 |

---

## 📊 方案一：只使用 Dashboard（推薦）

這是最簡單的方式，無需任何額外設置！

### 訪問 Dashboard

1. 在 VS Code 的「端口」面板中找到 **8501** 端口
2. 點擊地球圖標或右鍵 → "在瀏覽器中打開"
3. 你會看到 Streamlit Dashboard

### Dashboard 功能

- **實時日誌**: 查看 AI 的每一步行動和思考
- **思維狀態**: 當前目標和決策過程
- **技能樹**: 已學會的技能列表
- **統計分析**: 學習曲線和成功率圖表

### 優點

- ✅ 無需額外配置
- ✅ 完整觀察 AI 學習過程
- ✅ 不消耗 Minecraft 客戶端資源
- ✅ 可以在任何設備（手機/平板）上查看

---

## 🎮 方案二：連接 Minecraft 服務器

如果你想親自進入遊戲觀察 AI，需要設置端口轉發。

### A. 使用本地端口轉發（推薦）

這是最穩定的方式，將 Codespace 的端口轉發到你的本地電腦。

#### 步驟 1: 安裝 GitHub CLI

**macOS:**
```bash
brew install gh
```

**Windows (PowerShell):**
```powershell
winget install GitHub.cli
```

**Linux:**
```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh
```

#### 步驟 2: 認證

```bash
gh auth login
```

#### 步驟 3: 獲取 Codespace 名稱

在 Codespace 終端中執行：
```bash
echo $CODESPACE_NAME
```

或在本地執行：
```bash
gh codespace list
```

#### 步驟 4: 設置端口轉發

在你的**本地電腦**執行：

```bash
# 替換為你的 Codespace 名稱
gh codespace ports forward 25565:25565 -c YOUR_CODESPACE_NAME
```

保持此命令運行！

#### 步驟 5: 連接 Minecraft

1. 打開 Minecraft Java Edition 1.20.1
2. 多人遊戲 → 添加服務器
3. 服務器地址：`localhost:25565`
4. 進入服務器！

### B. 使用 VS Code 端口轉發

這種方式較不穩定，但無需安裝額外工具。

#### 步驟 1: 配置端口

1. 在 VS Code 中打開「端口」面板（Ports）
2. 找到 **25565** 端口
3. 右鍵點擊 → "端口可見性" → "公開"

#### 步驟 2: 獲取地址

右鍵點擊 25565 端口 → "複製本地地址"

格式類似：`*.github.dev:25565`

#### 步驟 3: 連接

在 Minecraft 中使用複製的地址作為服務器地址。

⚠️ **注意**: 這種方式可能不穩定，因為 GitHub 的代理更適合 HTTP 流量。

---

## 🔍 查看 AI 的實時思考

### 方法 1: 使用 Dashboard（推薦）

訪問 Dashboard 的「實時日誌」頁面，可以看到：

```
17:15:36 | 👁️ [OBSERVE] Gathering environment data...
17:15:36 |   位置: (-164.5, 76.0, -505.5)
17:15:36 |   生命值: 20/20
17:15:36 |   飢餓值: 20/20
17:15:36 | 🧠 [THINK] Consulting LLM for decision...
17:15:36 | 💭 LLM Decision: 尋找木頭資源
17:15:36 | ⚡ [ACT] Executing action...
```

### 方法 2: 使用終端日誌

在 Codespace 終端中執行：

```bash
# 實時查看所有日誌
docker-compose logs -f ai-bot

# 只看重要信息
docker-compose logs -f ai-bot | grep -E "(OBSERVE|THINK|ACT|ERROR)"

# 查看最近 50 條
docker-compose logs --tail=50 ai-bot
```

---

## 🛠️ 常用管理命令

### 查看服務狀態

```bash
docker-compose ps
```

### 重啟 AI Agent

```bash
docker-compose restart ai-bot
```

### 停止所有服務

```bash
docker-compose down
```

### 重新啟動

```bash
docker-compose up -d
```

### 健康檢查

```bash
./health_check.sh
```

### 創建備份

```bash
./backup.sh
```

### 查看特定服務日誌

```bash
# AI Agent
docker-compose logs -f ai-bot

# Minecraft Server
docker-compose logs -f mc-server

# Dashboard
docker-compose logs -f dashboard

# ChromaDB
docker-compose logs -f chromadb
```

---

## 🐛 常見問題

### Q: Dashboard 無法訪問？

**A**: 檢查端口轉發：

1. 打開 VS Code 的「端口」面板
2. 確認 8501 端口狀態為「正在運行」
3. 點擊地球圖標在瀏覽器中打開
4. 如果仍然無法訪問，執行：
   ```bash
   docker-compose restart dashboard
   ```

### Q: AI 一直顯示 "Wait and observe"？

**A**: 這可能是因為：

1. **觀察數據獲取失敗** - bot.js 與 Python 的通信有問題
2. **LLM 回應格式錯誤** - Ollama 返回的 JSON 無法解析

檢查日誌：
```bash
docker-compose logs --tail=100 ai-bot | grep ERROR
```

### Q: Minecraft 連接超時？

**A**: 在 Codespaces 環境中：

1. **優先使用 Dashboard 觀察** - 這是最穩定的方式
2. 如果必須連接遊戲，使用 `gh codespace ports forward`
3. 確保端口轉發命令保持運行狀態

### Q: Ollama 連接錯誤？

**A**: Ollama 在 Codespaces 中需要特殊配置：

```bash
# 檢查 Ollama 狀態
ps aux | grep ollama

# 如果沒有運行，重新啟動
pkill ollama
OLLAMA_HOST=0.0.0.0:11434 nohup ollama serve > ollama.log 2>&1 &

# 測試連接
curl http://localhost:11434/api/version
```

### Q: 容器無法啟動？

**A**: 檢查資源使用：

```bash
# 查看容器狀態
docker-compose ps

# 查看資源使用
docker stats --no-stream

# 查看錯誤日誌
docker-compose logs
```

如果記憶體不足，可以調整 Minecraft 服務器的記憶體：

編輯 `docker-compose.yml`:
```yaml
mc-server:
  environment:
    MEMORY: 2G  # 從 4G 降到 2G
```

---

## 📊 性能優化

### Codespaces 機器類型

- **2-core**: 最低配置，可運行但較慢
- **4-core**: 推薦配置，流暢運行
- **8-core**: 最佳性能

### 資源分配建議

```yaml
# docker-compose.yml
services:
  mc-server:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
  
  ai-bot:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### 使用更小的 AI 模型

在 `.env` 中：

```bash
# 使用更小更快的模型
LLM_MODEL=llama3.2:1b  # 或 phi3:mini

# 下載模型
ollama pull llama3.2:1b
```

---

## 🎯 推薦工作流程

### 1. 開發/測試階段

```bash
# 啟動系統
docker-compose up -d

# 開啟 Dashboard（瀏覽器）
# 端口 8501

# 開啟終端監控
docker-compose logs -f ai-bot

# 根據需要調整配置
nano .env
docker-compose restart ai-bot
```

### 2. 演示/展示階段

```bash
# 確保所有服務運行正常
./health_check.sh

# 在瀏覽器中打開 Dashboard
# 分享 Dashboard 的公開 URL

# 可選：如果需要遊戲內觀察
# 使用 gh codespace ports forward
```

### 3. 長時間運行

```bash
# 設置自動備份
crontab -e
# 添加：0 */6 * * * /workspaces/Project-Observer/backup.sh

# 監控資源使用
watch -n 60 docker stats --no-stream
```

---

## 🌐 端口映射參考

| 服務 | 容器端口 | 轉發端口 | 協議 | Codespaces 支持 |
|------|---------|---------|------|----------------|
| Minecraft | 25565 | 25565 | TCP | ⚠️ 需要設置 |
| Dashboard | 8501 | 8501 | HTTP | ✅ 自動 |
| ChromaDB | 8000 | 8000 | HTTP | ✅ 自動 |
| Ollama | 11434 | 11434 | HTTP | ✅ 內部 |

---

## 📞 獲取幫助

如果遇到問題：

1. **查看日誌**：`docker-compose logs -f ai-bot`
2. **健康檢查**：`./health_check.sh`
3. **查看文檔**：[DEPLOYMENT.md](DEPLOYMENT.md)
4. **提交 Issue**：[GitHub Issues](https://github.com/RainesTaiwan/Project-Observer/issues)

---

## 🎉 享受觀察 AI 學習的樂趣！

記住，在 Codespaces 中：
- ✅ **Dashboard 是你的最佳朋友** - 全功能觀察界面
- ✅ **終端日誌很實用** - 實時查看 AI 思考
- ⚠️ **Minecraft 連接需要額外設置** - 但不是必須的

祝你玩得開心！🚀
