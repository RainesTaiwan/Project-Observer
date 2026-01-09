# 🚀 快速開始指南

## 前置需求檢查

在開始之前，請確保你的系統已安裝：

- [ ] Docker (版本 20.10+)
- [ ] Docker Compose (版本 2.0+)
- [ ] OpenAI API Key (或本地 Ollama)

檢查命令：
```bash
docker --version
docker-compose --version
```

---

## 步驟 1：獲取項目

```bash
git clone https://github.com/RainesTaiwan/Project-Observer.git
cd Project-Observer
```

---

## 步驟 2：配置環境變量

```bash
# 複製環境變量模板
cp .env.example .env

# 編輯 .env 文件
nano .env  # 或使用你喜歡的編輯器
```

在 `.env` 文件中填入你的配置：

```env
# 必填：OpenAI API Key
OPENAI_API_KEY=sk-your-api-key-here

# 可選：使用其他模型
LLM_MODEL=gpt-4

# 可選：使用本地 Ollama
# OPENAI_API_BASE=http://host.docker.internal:11434/v1
# LLM_MODEL=llama3
```

---

## 步驟 3：啟動系統

```bash
# 方式一：使用啟動腳本（推薦）
chmod +x start.sh
./start.sh

# 方式二：直接使用 Docker Compose
docker-compose up -d --build
```

---

## 步驟 4：驗證運行狀態

等待 30-60 秒讓所有服務啟動，然後檢查：

```bash
# 查看容器狀態
docker-compose ps

# 查看 AI Agent 日誌
docker-compose logs -f ai-bot
```

你應該看到類似這樣的輸出：
```
✅ Bot connected as Agent_001
🔄 Entering main evolution loop...
👁️  [OBSERVE] Gathering environment data...
```

---

## 步驟 5：訪問儀表板

在瀏覽器中打開：**http://localhost:8501**

你會看到 AI 的實時思維過程！

---

## 步驟 6：進入遊戲（可選）

1. 啟動 Minecraft Java Edition 1.20.1
2. 點擊「多人遊戲」
3. 點擊「添加服務器」
4. 服務器地址填寫：`localhost`
5. 點擊「完成」並加入服務器

現在你可以在遊戲中看到 `Agent_001` 在探索世界了！

---

## 常用命令

```bash
# 查看實時日誌
./logs.sh

# 停止系統
./stop.sh

# 重啟 AI Agent
docker-compose restart ai-bot

# 查看所有容器狀態
docker-compose ps
```

---

## 故障排除

### 問題：容器無法啟動

```bash
# 查看錯誤日誌
docker-compose logs

# 重新構建鏡像
docker-compose down
docker-compose up -d --build
```

### 問題：AI 沒有反應

```bash
# 檢查 AI Agent 日誌
docker-compose logs ai-bot | tail -50

# 確認 API Key 是否正確
cat .env | grep OPENAI_API_KEY
```

### 問題：無法連接 Minecraft

```bash
# 檢查 Minecraft 服務器日誌
docker-compose logs mc-server

# 確認端口沒有被佔用
netstat -an | grep 25565
```

---

## 下一步

- 📖 閱讀完整文檔：[README.md](README.md)
- 🏗️ 了解項目結構：[STRUCTURE.md](STRUCTURE.md)
- ⚙️ 自定義 AI 行為：編輯 `agent_code/agent/llm_brain.py`
- 🎮 給 AI 添加新技能：在 `agent_skills/` 目錄添加 JSON 文件

---

祝你玩得開心！🎉
