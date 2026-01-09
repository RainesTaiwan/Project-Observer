# 項目結構

```
Project-Observer/
├── agent_code/                 # AI Agent 代碼
│   ├── agent/                  # 核心模組
│   │   ├── bot_controller.py   # Bot 控制器
│   │   ├── llm_brain.py        # LLM 思考引擎
│   │   ├── memory_manager.py   # 記憶管理
│   │   └── skill_manager.py    # 技能管理
│   ├── utils/
│   │   └── logger.py           # 日誌工具
│   ├── bot.js                  # Mineflayer Node.js 層
│   ├── main.py                 # 主程序
│   ├── Dockerfile
│   ├── package.json
│   └── requirements.txt
│
├── dashboard_code/             # 觀測儀表板
│   ├── app.py                  # Streamlit 應用
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml          # Docker 編排配置
├── .env.example                # 環境變量模板
├── .gitignore
│
├── start.sh                    # 啟動腳本
├── stop.sh                     # 停止腳本
├── logs.sh                     # 日誌查看腳本
│
└── README.md                   # 項目文檔
```

## 數據目錄 (運行時生成)

```
mc-data/                        # Minecraft 世界數據
chroma-data/                    # 向量數據庫
agent_skills/                   # AI 學會的技能
agent_logs/                     # 運行日誌
agent_memory/                   # 記憶數據
```
