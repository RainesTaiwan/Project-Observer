#!/bin/bash

# Project Observer - 停止腳本

echo "🛑 Stopping Project Observer..."

docker-compose down

echo "✅ All services stopped."
echo ""
echo "💡 To remove all data (including world and memories):"
echo "   rm -rf mc-data chroma-data agent_skills agent_logs agent_memory"
