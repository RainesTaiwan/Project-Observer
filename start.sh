#!/bin/bash

# Project Observer - 快速啟動腳本

echo "🤖 Project Observer - Starting System"
echo "========================================"

# 檢查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your OPENAI_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# 檢查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# 創建必要的目錄
echo "📁 Creating necessary directories..."
mkdir -p mc-data chroma-data agent_skills agent_logs agent_memory

# 構建並啟動容器
echo "🚀 Building and starting containers..."
docker-compose up -d --build

# 等待服務啟動
echo "⏳ Waiting for services to start..."
sleep 10

# 顯示狀態
echo ""
echo "✅ System started successfully!"
echo "========================================"
echo "📊 Dashboard:    http://localhost:8501"
echo "🎮 Minecraft:    localhost:25565"
echo "💾 ChromaDB:     http://localhost:8000"
echo "========================================"
echo ""
echo "📋 Useful commands:"
echo "  View logs:        docker-compose logs -f ai-bot"
echo "  Stop system:      docker-compose down"
echo "  Restart AI:       docker-compose restart ai-bot"
echo ""
echo "🎮 Connect to Minecraft:"
echo "  1. Open your Minecraft client (Java Edition 1.20.1)"
echo "  2. Go to Multiplayer -> Add Server"
echo "  3. Server Address: localhost"
echo "  4. Click 'Join Server'"
echo ""
echo "Happy observing! 🔬"
