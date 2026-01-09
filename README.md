# 🤖 Project Observer

> **觀察 AI 從零開始在 Minecraft 世界中學習生存、採集、戰鬥與建造**

一個革命性的 AI 觀測系統，讓你見證人工智能如何在開放世界遊戲中自主學習和進化。完全支援本地 AI（Ollama）或雲端 AI（OpenAI）。

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Docker](https://img.shields.io/badge/docker-required-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Node.js](https://img.shields.io/badge/node-18-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📖 目錄

- [系統概述](#-系統概述)
- [快速開始](#-快速開始)
- [環境需求](#-環境需求)
- [啟動方式](#-啟動方式)
- [使用指南](#-使用指南)
- [系統架構](#-系統架構)
- [進階配置](#-進階配置)
- [開發說明](#-開發說明)
- [常見問題](#-常見問題)

---

## 🎯 系統概述

**Project Observer** 是一個完整的 AI 觀測生態系統，由四個核心容器組成：

1. **🎮 Minecraft Server** - AI 和玩家共存的虛擬世界
2. **🧠 AI Agent** - 智能代理核心（感知、思考、行動、學習）
3. **💾 Vector Database** - AI 的長期記憶存儲（ChromaDB）
4. **📊 Dashboard** - 實時觀測 AI 的思維過程（Streamlit）

### 核心機制：The Evolution Loop

```
觀察 (Observe) → 思考 (Think) → 行動 (Act) → 反思 (Reflect) → 學習 (Learn)
     ↑                                                              ↓
     └──────────────────────── 持續進化 ────────────────────────────┘
```

**AI 能力**：
- 🔍 **感知環境**：檢測周圍方塊、生物、資源、健康狀態
- 🧠 **智能決策**：使用 LLM（GPT-4 或 Llama 3）進行推理
- ⚡ **動態編程**：根據情況生成並執行 JavaScript 代碼
- 📚 **持續學習**：從成功和失敗中學習，建立技能庫
- 🎯 **第一人稱視角**：透過 Prismarine Viewer 觀看 AI 的視角

---

## ✨ 核心特性

### 🎓 自主學習
- ✅ 從零開始，無預設行為
- ✅ 根據執行結果自動修正策略
- ✅ 成功的技能會被永久保存
- ✅ 失敗的經驗會被記憶並避免重複

### 🧠 智能思考
- ✅ 使用大型語言模型進行決策
- ✅ 支持 OpenAI GPT-4 或本地 Ollama
- ✅ 上下文感知的動作規劃
- ✅ 基於過去經驗的記憶檢索

### 🔬 完全可觀測
- ✅ 實時查看 AI 的"內心獨白"
- ✅ 技能樹可視化
- ✅ 學習曲線圖表
- ✅ 詳細的日誌記錄

### 🎮 人類互動
- ✅ 你可以隨時加入遊戲
- ✅ 觀察 AI 的行為
- ✅ 給予物品或提示
- ✅ 與 AI 共同建造

---

## 🏗️ 系統架構

```
┌─────────────┐
│ 人類玩家    │ ──── Port 25565 ───┐
└─────────────┘                     │
                                    ▼
┌────────────────────────────────────────────────┐
│           Docker Compose Network               │
│                                                │
│  ┌──────────────┐       ┌──────────────┐     │
│  │ Minecraft    │◄──────┤   AI Agent   │     │
│  │   Server     │       │   (大腦)     │     │
│  └──────────────┘       └──────┬───────┘     │
│                                 │             │
│                         ┌───────▼────────┐    │
│                         │ Vector Database│    │
│                         │   (記憶庫)     │    │
│                         └────────────────┘    │
│                                                │
│  ┌──────────────┐                             │
│  │  Dashboard   │◄────讀取日誌/狀態───────────┤
│  │ (觀測面板)   │                             │
│  └──────────────┘                             │
│         │                                      │
└─────────┼──────────────────────────────────────┘
          │
     Port 8501
          ▼
   ┌──────────────┐
   │ 瀏覽器觀測   │
   └──────────────┘
```

---

## 🚀 快速開始

### 環境需求

#### 軟體需求
- **Docker** 20.10+ & **Docker Compose** 2.0+ (必須)
- **OpenAI API Key** 或 **Ollama** (二選一，推薦使用免費的 Ollama)
- **Minecraft Java Edition 1.20.1** (可選，用於人類玩家進入觀測)

#### 硬體需求 
- **最低配置**: 4核 CPU + 8GB RAM + 20GB 儲存空間
- **推薦配置**: 6核 CPU + 16GB RAM + 50GB 儲存空間
- **本地 AI 配置**: 8核 CPU + 16GB RAM (用於 Ollama Llama 3.1 8B)
- **詳細說明**: 查看 [HARDWARE_REQUIREMENTS.md](HARDWARE_REQUIREMENTS.md)

---

## 📦 啟動方式

### 方法一：使用本地 AI（Ollama - 推薦，完全免費）

```bash
# 1. Clone 專案
git clone https://github.com/RainesTaiwan/Project-Observer.git
cd Project-Observer

# 2. 一鍵設置本地 AI（會自動安裝 Ollama 並下載模型）
chmod +x setup_local_ai.sh
./setup_local_ai.sh

# 3. 啟動系統
./start.sh
```

**Ollama 優勢**：
- ✅ 完全免費，無 API 費用
- ✅ 數據隱私，在本地運行
- ✅ 無速率限制
- ✅ 支援多種模型：Llama 3.1 8B、Mistral 7B、Qwen 2.5 7B
- 📖 更多信息：[LOCAL_AI_GUIDE.md](LOCAL_AI_GUIDE.md)

### 方法二：使用 OpenAI API

```bash
# 1. Clone 專案
git clone https://github.com/RainesTaiwan/Project-Observer.git
cd Project-Observer

# 2. 配置環境變量
cp .env.example .env
nano .env  # 填入你的 OPENAI_API_KEY

# 3. 啟動系統
chmod +x start.sh
./start.sh
```

### 方法三：使用 Makefile（推薦開發者使用）

```bash
# 查看所有可用命令
make help

# 快速啟動
make start

# 查看日誌
make logs

# 停止系統
make stop

# 完整清理
make clean
```

### 方法四：在 GitHub Codespaces 中運行（雲端開發）

1. Fork 此倉庫到你的 GitHub
2. 點擊 "Code" → "Codespaces" → "Create codespace"
3. 等待環境自動配置完成
4. 運行 `./setup_local_ai.sh && ./start.sh`

📖 詳細說明：[CODESPACES_GUIDE.md](CODESPACES_GUIDE.md)

---

## 🌐 系統訪問

啟動成功後，可以訪問以下服務：

| 服務 | 地址 | 說明 |
|------|------|------|
| 📊 **Dashboard** | http://localhost:8501 | AI 觀測儀表板（實時日誌、思維狀態、技能樹、統計） |
| 🎥 **第一人稱視角** | http://localhost:3000 | AI 的實時第一人稱視角（Prismarine Viewer） |
| 🎮 **Minecraft 伺服器** | localhost:25565 | 遊戲伺服器（人類玩家可以連入觀測） |
| 💾 **ChromaDB** | http://localhost:8000 | 向量數據庫 API（AI 的記憶存儲） |

---

## 📚 使用指南

### 步驟一：觀察 AI 啟動

打開瀏覽器訪問 **http://localhost:8501**，你會看到：

- 🔴 **實時日誌** - AI 的每一步行動和決策過程
- 🧠 **思維狀態** - 當前目標、位置、健康狀況
- 🎯 **技能樹** - 已學會的技能列表和成功率
- 📈 **統計分析** - 學習曲線、成功率、行動歷史

### 步驟二：觀看 AI 第一人稱視角

訪問 **http://localhost:3000**，你會看到：

- 🎥 AI 眼中的實時畫面
- 🎮 可以用滑鼠旋轉視角
- 📍 AI 的當前位置和狀態
- 💡 適合用於直播或錄製影片

### 步驟三：進入遊戲與 AI 互動（可選）

1. 打開你的 Minecraft 客戶端（**Java 版 1.20.1**）
2. 多人遊戲 → 添加伺服器
3. 伺服器地址：`localhost`
4. 進入伺服器，找到 AI 玩家 `Agent_001`

**你可以**：
- 跟隨 AI 觀察它的行為
- 給 AI 物品測試它的反應
- 在聊天中與 AI 溝通（需額外配置）
- 清理怪物保護 AI

### 步驟四：觀察學習進化

打開 Dashboard 的 **技能樹** 頁面，觀察 AI 的學習過程：

1. **首次行動**：AI 遇到新任務時會動態生成代碼
2. **執行測試**：嘗試執行並記錄結果
3. **成功保存**：成功的技能會保存到 `agent_skills/` 目錄
4. **重複使用**：下次遇到類似情況時直接調用已有技能
5. **失敗學習**：失敗的嘗試會被記錄，AI 會調整策略避免重複錯誤

---

## 🔧 常用命令

### 啟動與停止

```bash
# 啟動系統
./start.sh

# 停止系統
./stop.sh
# 或
docker-compose down

# 重啟 AI
docker-compose restart ai-bot

# 重新構建並啟動
docker-compose up -d --build
```

### 查看日誌

```bash
# 所有服務日誌
docker-compose logs -f

# 只看 AI 日誌
docker-compose logs -f ai-bot

# 查看 Minecraft 伺服器日誌
docker-compose logs -f mc-server

# 使用日誌腳本（互動式選單）
./logs.sh
```

### 健康檢查

```bash
# 運行完整健康檢查
./health_check.sh

# 檢查容器狀態
docker-compose ps

# 檢查資源使用
docker stats
```

### 備份與恢復

```bash
# 創建備份
./backup.sh

# 恢復備份
./restore.sh ./backups/backup_20260109_120000

# 查看所有備份
ls -lh backups/
```

---

## 📖 完整文檔索引

### 快速入門
- 📋 [QUICKSTART.md](QUICKSTART.md) - 5分鐘快速上手指南
- 🚀 [INSTALLATION.md](INSTALLATION.md) - 詳細安裝步驟
- ☁️ [CODESPACES_GUIDE.md](CODESPACES_GUIDE.md) - GitHub Codespaces 雲端部署

### AI 配置
- 🧠 [LOCAL_AI_GUIDE.md](LOCAL_AI_GUIDE.md) - 本地 AI（Ollama）完整指南
- 🆚 [OPENAI_VS_LOCAL.md](OPENAI_VS_LOCAL.md) - OpenAI vs 本地 AI 對比分析
- 🔧 [DEPLOYMENT.md](DEPLOYMENT.md) - 生產環境部署指南

### 直播與觀測
- 🎥 [STREAMING_GUIDE.md](STREAMING_GUIDE.md) - 第一人稱視角直播設置
- 📊 [Dashboard 使用說明](#-系統訪問) - 儀表板功能介紹

### 開發文檔
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - 系統架構設計
- 📁 [STRUCTURE.md](STRUCTURE.md) - 專案結構說明
- 🔌 [HARDWARE_REQUIREMENTS.md](HARDWARE_REQUIREMENTS.md) - 硬體需求詳解
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - 貢獻指南
- 📝 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 專案摘要

---

## ⚙️ 進階配置

### 使用本地 AI（Ollama）- 完全免費！

**為什麼選擇本地 AI？**
- 💰 完全免費，無 API 費用
- 🔒 數據隱私，完全本地運行
- ⚡ 無限制調用，無速率限制
- 🎯 可訓練專屬模型

**一鍵設置：**

```bash
# 自動安裝並配置 Ollama
chmod +x setup_local_ai.sh
./setup_local_ai.sh

# 腳本會自動：
# 1. 安裝 Ollama
# 2. 讓你選擇模型（Llama 3.1 8B、Mistral 7B 等）
# 3. 下載模型
# 4. 配置 .env 文件
# 5. 測試連接
```

**手動設置：**

```bash
# 1. 安裝 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下載模型（選一個）
ollama pull llama3.1:8b      # 推薦：平衡性能 (4.9GB)
ollama pull llama3.2:3b      # 輕量級，更快 (2GB)
ollama pull mistral:7b       # 高質量輸出 (4.1GB)
ollama pull qwen2.5:7b       # 中文優化 (4.4GB)

# 3. 啟動 Ollama
ollama serve

# 4. 修改 .env
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.1:8b
OPENAI_API_KEY=ollama
```

📖 **詳細指南**：[LOCAL_AI_GUIDE.md](LOCAL_AI_GUIDE.md)

### 自定義 AI 行為

編輯 `agent_code/agent/llm_brain.py` 中的系統提示詞：

```python
# 例如：讓 AI 專注於建造
system_prompt = """
你是一個 Minecraft 建築專家 AI。
當前目標：建造複雜的建築結構。

可用行動：explore, mine_wood, mine_stone, hunt, retreat, rest

優先順序：
1. 收集建築材料（木頭、石頭）
2. 規劃建築藍圖
3. 執行建造
"""
```

### 調整決策頻率

修改 `agent_code/main.py` 的主循環：

```python
# 更快的決策速度（預設 5 秒）
time.sleep(2)

# 極速模式（小心 CPU 使用率）
time.sleep(0)
```

---

## 🛠️ 開發說明

### 專案結構

詳見 [STRUCTURE.md](STRUCTURE.md)

```bash
# 查看日誌
./logs.sh

# 停止系統
./stop.sh

# 重啟 AI Agent
docker-compose restart ai-bot

# 重建容器
docker-compose up -d --build

# 清除所有數據（警告：會刪除世界和記憶）
rm -rf mc-data chroma-data agent_skills agent_logs agent_memory
```

### 🚀 生產環境部署

詳細的部署指南請查看 [DEPLOYMENT.md](DEPLOYMENT.md)，包含：

- 📦 **本地部署** - 快速測試環境
- 🌐 **VPS/雲端部署** - DigitalOcean, AWS, GCP, Linode
- 🚢 **Docker Swarm** - 多機分佈式部署
- ☸️ **Kubernetes** - 企業級大規模部署
- 🔒 **安全性配置** - 防火牆、SSL、權限管理
- 📊 **監控與維護** - Prometheus, Grafana, 健康檢查
- 💾 **備份與恢復** - 自動化備份腳本

**快速命令**：
```bash
# 健康檢查
./health_check.sh

# 創建備份
./backup.sh

# 恢復備份
./restore.sh /path/to/backup

# 生產環境啟動
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 技能開發

AI 學會的技能保存在 `agent_skills/` 目錄，格式如下：

```json
{
  "name": "mine_wood",
  "goal": "獲取木頭",
  "code": "await mineBlock('oak_log');",
  "success_count": 15,
  "failure_count": 2
}
```

你可以手動添加技能來"教導" AI。

---

## ❓ 常見問題

### Q: AI 一直站著不動？

**A:** 檢查以下幾點：
1. LLM API 是否正常（查看日誌）
2. OPENAI_API_KEY 是否正確
3. 是否有網路連接問題

```bash
docker-compose logs ai-bot | grep ERROR
```

### Q: Minecraft 服務器啟動很慢？

**A:** 第一次啟動時，服務器需要下載並安裝 Fabric。這可能需要 3-5 分鐘。後續啟動會快很多。

### Q: AI 總是做同樣的事情？

**A:** 這可能是因為：
1. 記憶數據庫中已有成功經驗
2. AI 認為這是最優策略

你可以清空記憶重新訓練：
```bash
rm -rf chroma-data agent_skills agent_memory
docker-compose restart ai-bot
```

### Q: 如何讓 AI 更聰明？

**A:** 嘗試以下方法：
1. 使用更強的模型（如 `gpt-4-turbo`）
2. 增加記憶檢索數量（修改 `top_k` 參數）
3. 優化系統提示詞

### Q: 可以多個 AI 同時運行嗎？

**A:** 可以！複製 `docker-compose.yml` 中的 `ai-bot` 服務，修改容器名稱和 BOT_USERNAME 即可。

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

如果你有任何想法或改進建議，請：
1. Fork 這個專案
2. 創建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. Push 到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

---

## 📜 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件。

---

## 🌟 致謝

- [Mineflayer](https://github.com/PrismarineJS/mineflayer) - Minecraft Bot 框架
- [itzg/minecraft-server](https://github.com/itzg/docker-minecraft-server) - Docker Minecraft 鏡像
- [ChromaDB](https://www.trychroma.com/) - 向量數據庫
- [Streamlit](https://streamlit.io/) - Dashboard 框架
- [Voyager](https://voyager.minedojo.org/) - AI Minecraft Agent 靈感來源

---

## 📞 聯繫

- GitHub: [@RainesTaiwan](https://github.com/RainesTaiwan)
- Project Link: [https://github.com/RainesTaiwan/Project-Observer](https://github.com/RainesTaiwan/Project-Observer)

---

<div align="center">

**⭐ 如果這個專案對你有幫助，請給一個星星！⭐**

Made with ❤️ by AI Enthusiasts

</div>