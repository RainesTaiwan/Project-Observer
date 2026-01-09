#!/bin/bash

# Project Observer - 查看日誌腳本

echo "📋 Project Observer - Log Viewer"
echo "================================"
echo ""
echo "選擇要查看的日誌:"
echo "  1) AI Agent"
echo "  2) Minecraft Server"
echo "  3) Dashboard"
echo "  4) ChromaDB"
echo "  5) All services"
echo ""

read -p "輸入選項 (1-5): " choice

case $choice in
    1)
        echo "📊 AI Agent logs:"
        docker-compose logs -f ai-bot
        ;;
    2)
        echo "🎮 Minecraft Server logs:"
        docker-compose logs -f mc-server
        ;;
    3)
        echo "📈 Dashboard logs:"
        docker-compose logs -f dashboard
        ;;
    4)
        echo "💾 ChromaDB logs:"
        docker-compose logs -f chromadb
        ;;
    5)
        echo "📋 All logs:"
        docker-compose logs -f
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac
