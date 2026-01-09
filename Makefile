.PHONY: help install start stop restart logs logs-ai logs-mc logs-dashboard status clean clean-all build shell-ai shell-mc

# 默認目標
help:
	@echo "🤖 Project Observer - 可用命令"
	@echo "================================"
	@echo ""
	@echo "  make install        - 初始化項目（首次使用）"
	@echo "  make start          - 啟動所有服務"
	@echo "  make stop           - 停止所有服務"
	@echo "  make restart        - 重啟所有服務"
	@echo ""
	@echo "  make logs           - 查看所有日誌"
	@echo "  make logs-ai        - 查看 AI Agent 日誌"
	@echo "  make logs-mc        - 查看 Minecraft 日誌"
	@echo "  make logs-dashboard - 查看 Dashboard 日誌"
	@echo ""
	@echo "  make status         - 查看容器狀態"
	@echo "  make build          - 重新構建鏡像"
	@echo ""
	@echo "  make shell-ai       - 進入 AI Agent 容器"
	@echo "  make shell-mc       - 進入 Minecraft 容器"
	@echo ""
	@echo "  make clean          - 停止並刪除容器"
	@echo "  make clean-all      - 刪除所有數據（危險！）"
	@echo ""

# 初始化項目
install:
	@echo "📦 初始化 Project Observer..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ 已創建 .env 文件"; \
		echo "⚠️  請編輯 .env 並填入你的 OPENAI_API_KEY"; \
		echo ""; \
		echo "   nano .env"; \
		echo ""; \
	else \
		echo "✅ .env 文件已存在"; \
	fi
	@mkdir -p mc-data chroma-data agent_skills agent_logs agent_memory
	@echo "✅ 已創建數據目錄"
	@echo ""
	@echo "🚀 運行以下命令啟動系統："
	@echo "   make start"

# 啟動服務
start:
	@echo "🚀 啟動 Project Observer..."
	@docker-compose up -d --build
	@echo ""
	@echo "⏳ 等待服務啟動（30秒）..."
	@sleep 10
	@echo ""
	@$(MAKE) status
	@echo ""
	@echo "✅ 系統已啟動！"
	@echo ""
	@echo "📊 Dashboard:    http://localhost:8501"
	@echo "🎮 Minecraft:    localhost:25565"
	@echo "💾 ChromaDB:     http://localhost:8000"
	@echo ""
	@echo "查看日誌: make logs-ai"

# 停止服務
stop:
	@echo "🛑 停止 Project Observer..."
	@docker-compose down
	@echo "✅ 所有服務已停止"

# 重啟服務
restart:
	@echo "🔄 重啟 Project Observer..."
	@docker-compose restart
	@echo "✅ 服務已重啟"

# 查看所有日誌
logs:
	@docker-compose logs -f

# 查看 AI Agent 日誌
logs-ai:
	@echo "📋 AI Agent 日誌（按 Ctrl+C 退出）:"
	@docker-compose logs -f ai-bot

# 查看 Minecraft 日誌
logs-mc:
	@echo "📋 Minecraft Server 日誌（按 Ctrl+C 退出）:"
	@docker-compose logs -f mc-server

# 查看 Dashboard 日誌
logs-dashboard:
	@echo "📋 Dashboard 日誌（按 Ctrl+C 退出）:"
	@docker-compose logs -f dashboard

# 查看容器狀態
status:
	@echo "📊 容器狀態:"
	@docker-compose ps

# 重新構建鏡像
build:
	@echo "🔨 重新構建鏡像..."
	@docker-compose build --no-cache
	@echo "✅ 構建完成"

# 進入 AI Agent 容器
shell-ai:
	@echo "🐚 進入 AI Agent 容器..."
	@docker-compose exec ai-bot /bin/bash

# 進入 Minecraft 容器
shell-mc:
	@echo "🐚 進入 Minecraft 容器..."
	@docker-compose exec mc-server /bin/bash

# 清理容器
clean:
	@echo "🧹 清理容器..."
	@docker-compose down -v
	@echo "✅ 容器已清理"

# 清理所有數據（危險！）
clean-all:
	@echo "⚠️  警告：這將刪除所有數據（世界、技能、記憶）！"
	@echo "按 Ctrl+C 取消，或按 Enter 繼續..."
	@read confirm
	@echo "🧹 刪除所有數據..."
	@docker-compose down -v
	@rm -rf mc-data chroma-data agent_skills agent_logs agent_memory
	@echo "✅ 所有數據已刪除"
	@echo ""
	@echo "重新開始: make install"
