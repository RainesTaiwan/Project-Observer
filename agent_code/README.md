# Agent Code

這個目錄包含 AI 代理人的核心代碼。

## 結構

```
agent_code/
├── agent/                  # AI 核心模組
│   ├── bot_controller.py   # Minecraft Bot 控制器
│   ├── llm_brain.py        # LLM 思考引擎
│   ├── memory_manager.py   # 記憶管理器
│   └── skill_manager.py    # 技能管理器
├── utils/                  # 工具函數
│   └── logger.py           # 日誌配置
├── bot.js                  # Mineflayer Node.js 層
├── main.py                 # 主程序入口
├── Dockerfile              # Docker 鏡像定義
├── package.json            # Node.js 依賴
└── requirements.txt        # Python 依賴
```

## 運行邏輯

1. `main.py` 啟動主循環
2. `bot_controller.py` 通過 `bot.js` 與 Minecraft 交互
3. `llm_brain.py` 調用 LLM 進行決策
4. `memory_manager.py` 存取長期記憶
5. `skill_manager.py` 管理學會的技能
