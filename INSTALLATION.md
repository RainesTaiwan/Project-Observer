# 🚀 Project Observer - 詳細安裝指南

## 目錄
- [系統需求](#系統需求)
- [安裝步驟](#安裝步驟)
- [配置說明](#配置說明)
- [啟動系統](#啟動系統)
- [驗證安裝](#驗證安裝)
- [故障排除](#故障排除)

---

## 系統需求

### 必需軟體
- **Docker**: 版本 20.10 或更高
- **Docker Compose**: 版本 2.0 或更高
- **Git**: 用於克隆項目

### 硬體需求
- **CPU**: 4 核心或更多（推薦）
- **內存**: 至少 4GB RAM（推薦 8GB）
- **磁盤**: 至少 5GB 可用空間
- **網路**: 穩定的網際網路連接

### 可選軟體
- **Minecraft Java Edition 1.20.1**: 如果你想進入遊戲觀測
- **Ollama**: 如果你想使用本地 LLM

### 支持的操作系統
- ✅ Linux (Ubuntu 20.04+, Debian 11+, etc.)
- ✅ macOS (10.15+)
- ✅ Windows 10/11 (with WSL2)

---

## 安裝步驟

### 1. 安裝 Docker 和 Docker Compose

#### Linux (Ubuntu/Debian)
```bash
# 更新包列表
sudo apt update

# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 將當前用戶添加到 docker 組
sudo usermod -aG docker $USER

# 安裝 Docker Compose
sudo apt install docker-compose-plugin

# 驗證安裝
docker --version
docker compose version
```

#### macOS
```bash
# 使用 Homebrew 安裝
brew install --cask docker

# 或者從官網下載 Docker Desktop
# https://www.docker.com/products/docker-desktop
```

#### Windows (WSL2)
```powershell
# 安裝 Docker Desktop for Windows
# https://www.docker.com/products/docker-desktop

# 確保啟用 WSL2 後端
```

### 2. 克隆項目

```bash
# 使用 HTTPS
git clone https://github.com/RainesTaiwan/Project-Observer.git

# 或使用 SSH
git clone git@github.com:RainesTaiwan/Project-Observer.git

# 進入項目目錄
cd Project-Observer
```

### 3. 檢查文件完整性

```bash
# 確認所有必要文件存在
ls -la

# 應該看到：
# docker-compose.yml
# .env.example
# agent_code/
# dashboard_code/
# start.sh, stop.sh, logs.sh
```

---

## 配置說明

### 1. 創建環境變量文件

```bash
# 複製模板
cp .env.example .env

# 編輯文件
nano .env  # 或使用 vim, code, etc.
```

### 2. 配置 OpenAI API

在 `.env` 文件中填入：

```env
# 必填：OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 推薦使用 GPT-4
LLM_MODEL=gpt-4

# 或使用 GPT-3.5 (更便宜)
# LLM_MODEL=gpt-3.5-turbo
```

**獲取 API Key:**
1. 訪問 https://platform.openai.com/api-keys
2. 登入或註冊帳號
3. 創建新的 API Key
4. 複製並粘貼到 `.env` 文件

### 3. 配置本地 LLM (可選)

如果你想使用本地 Ollama 而不是 OpenAI：

```bash
# 安裝 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下載模型
ollama pull llama3

# 啟動 Ollama 服務
ollama serve
```

修改 `.env`:
```env
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3
OPENAI_API_KEY=ollama  # 任意值即可
```

### 4. 其他可選配置

```env
# Minecraft 配置
MC_VERSION=1.20.1
MC_DIFFICULTY=normal
MC_MAX_MEMORY=2G

# Bot 配置
BOT_USERNAME=Agent_001
LOG_LEVEL=INFO
```

---

## 啟動系統

### 方式一：使用啟動腳本（推薦）

```bash
# 賦予執行權限
chmod +x start.sh stop.sh logs.sh

# 啟動系統
./start.sh
```

### 方式二：使用 Make 命令

```bash
# 初始化（首次使用）
make install

# 啟動服務
make start
```

### 方式三：使用 Docker Compose

```bash
# 構建並啟動
docker-compose up -d --build

# 查看日誌
docker-compose logs -f
```

### 等待啟動

系統需要 **1-3 分鐘** 來完全啟動：

```bash
# 查看容器狀態
docker-compose ps

# 等待所有容器都顯示 "Up" 或 "Up (healthy)"
```

---

## 驗證安裝

### 1. 檢查容器狀態

```bash
docker-compose ps
```

預期輸出：
```
NAME                  STATUS
mc-world              Up (healthy)
ai-memory             Up
steve-gpt             Up
observer-dashboard    Up
```

### 2. 檢查 Dashboard

在瀏覽器中打開：**http://localhost:8501**

你應該看到：
- 🤖 Project Observer 標題
- 實時日誌更新
- 各個功能 Tab

### 3. 檢查 AI Agent 日誌

```bash
# 方式一
./logs.sh
# 選擇選項 1

# 方式二
make logs-ai

# 方式三
docker-compose logs -f ai-bot
```

預期看到：
```
✅ Bot connected as Agent_001
🔄 Entering main evolution loop...
👁️  [OBSERVE] Gathering environment data...
```

### 4. 測試 Minecraft 連接（可選）

1. 啟動 Minecraft Java Edition 1.20.1
2. 點擊「多人遊戲」
3. 點擊「添加服務器」
4. 服務器地址：`localhost`
5. 加入服務器

你應該看到 `Agent_001` 在遊戲世界中！

---

## 故障排除

### 問題 1: Docker 命令需要 sudo

**原因**: 當前用戶不在 docker 組中

**解決方案**:
```bash
sudo usermod -aG docker $USER
newgrp docker

# 或重新登入
```

### 問題 2: 端口已被佔用

**錯誤信息**: `Bind for 0.0.0.0:25565 failed: port is already allocated`

**解決方案**:
```bash
# 查找佔用端口的進程
sudo lsof -i :25565
sudo lsof -i :8501
sudo lsof -i :8000

# 停止相關服務或修改 docker-compose.yml 中的端口映射
```

### 問題 3: AI Agent 無法連接 Minecraft

**檢查步驟**:
```bash
# 1. 確認 Minecraft 服務器已啟動
docker-compose logs mc-server | grep "Done"

# 2. 檢查網路連接
docker network ls
docker network inspect project-observer-network

# 3. 重啟 AI Agent
docker-compose restart ai-bot
```

### 問題 4: LLM API 調用失敗

**可能原因**:
- API Key 無效或過期
- 網路連接問題
- API 限額已用完

**解決方案**:
```bash
# 1. 驗證 API Key
cat .env | grep OPENAI_API_KEY

# 2. 測試 API 連接
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# 3. 查看 AI Agent 錯誤日誌
docker-compose logs ai-bot | grep ERROR
```

### 問題 5: Dashboard 無法訪問

**檢查步驟**:
```bash
# 1. 確認容器運行
docker-compose ps dashboard

# 2. 查看 Dashboard 日誌
docker-compose logs dashboard

# 3. 檢查端口
curl http://localhost:8501

# 4. 重啟 Dashboard
docker-compose restart dashboard
```

### 問題 6: 磁盤空間不足

**解決方案**:
```bash
# 清理未使用的 Docker 資源
docker system prune -a

# 查看磁盤使用
docker system df

# 清理項目數據（警告：會刪除 AI 學習的內容）
make clean-all
```

### 問題 7: 記憶體不足

**症狀**: 容器頻繁重啟或崩潰

**解決方案**:
```bash
# 1. 檢查系統記憶體
free -h

# 2. 減少 Minecraft 服務器記憶體
# 編輯 docker-compose.yml
MAX_MEMORY: "1G"  # 從 2G 改為 1G

# 3. 重啟服務
docker-compose restart
```

### 問題 8: 容器構建失敗

**解決方案**:
```bash
# 1. 清理構建緩存
docker-compose build --no-cache

# 2. 檢查 Dockerfile 語法
docker-compose config

# 3. 查看詳細錯誤
docker-compose up --build
```

---

## 高級配置

### 多 AI Agent 部署

編輯 `docker-compose.yml`，添加第二個 Agent：

```yaml
ai-bot-2:
  build: ./agent_code
  container_name: steve-gpt-2
  depends_on:
    - mc-server
    - chromadb
  environment:
    BOT_USERNAME: "Agent_002"
    # ... 其他配置相同
```

### 自定義 Minecraft 配置

編輯 `docker-compose.yml`:

```yaml
mc-server:
  environment:
    DIFFICULTY: "hard"          # easy, normal, hard
    VIEW_DISTANCE: "16"         # 渲染距離
    MAX_PLAYERS: "10"           # 最大玩家數
    ENABLE_COMMAND_BLOCK: "true"
```

### 啟用更多日誌

修改 `.env`:
```env
LOG_LEVEL=DEBUG  # 顯示更詳細的日誌
```

---

## 卸載

### 停止並刪除所有容器

```bash
# 停止服務
docker-compose down

# 刪除數據卷
docker-compose down -v
```

### 刪除所有數據

```bash
# 使用 Make
make clean-all

# 或手動刪除
rm -rf mc-data chroma-data agent_skills agent_logs agent_memory
```

### 完全卸載

```bash
# 刪除項目
cd ..
rm -rf Project-Observer

# 卸載 Docker (可選)
sudo apt remove docker-ce docker-ce-cli containerd.io
```

---

## 下一步

安裝成功後：

1. 📖 閱讀 [README.md](README.md) 了解系統功能
2. 🎮 閱讀 [使用指南](README.md#使用指南) 學習如何與 AI 互動
3. ⚙️ 閱讀 [進階配置](README.md#進階配置) 自定義 AI 行為
4. 🏗️ 閱讀 [ARCHITECTURE.md](ARCHITECTURE.md) 理解系統架構

---

## 獲取幫助

- 📖 文檔: [README.md](README.md)
- 🐛 Bug 報告: [GitHub Issues](https://github.com/RainesTaiwan/Project-Observer/issues)
- 💬 討論: [GitHub Discussions](https://github.com/RainesTaiwan/Project-Observer/discussions)

---

祝你觀測愉快！🔬✨
