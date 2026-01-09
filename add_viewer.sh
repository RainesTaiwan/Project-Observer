#!/bin/bash

# 🎥 自動添加第一視角功能到 AI Bot

set -e

echo "🎥 正在添加第一視角功能..."

# 1. 安裝 Prismarine Viewer
echo "📦 安裝 prismarine-viewer..."
cd agent_code
npm install prismarine-viewer

# 2. 備份原始文件
echo "💾 備份 bot.js..."
cp bot.js bot.js.backup

# 3. 檢查是否已經添加過
if grep -q "prismarine-viewer" bot.js; then
    echo "⚠️  檢測到已經添加過 viewer 功能"
    echo "如需重新添加，請先刪除 bot.js 並從 bot.js.backup 恢復"
    exit 0
fi

# 4. 在文件頂部添加 import
echo "📝 添加 import 語句..."
sed -i '1i const mineflayerViewer = require("prismarine-viewer").mineflayer;' bot.js

# 5. 在 spawn 事件中添加 viewer 啟動代碼
echo "📝 添加 viewer 啟動代碼..."
sed -i "/bot.once('spawn'/a \    \n    // 🎥 啟動第一視角查看器\n    mineflayerViewer(bot, { port: 3000, firstPerson: true });\n    console.log('🎥 First-person viewer started at http://localhost:3000');" bot.js

# 6. 更新 Docker Compose
echo "🐳 更新 docker-compose.yml..."
cd ..

if grep -q "3000:3000" docker-compose.yml; then
    echo "⚠️  端口映射已存在"
else
    # 在 ai-bot 服務的 ports 部分添加 3000 端口
    if grep -A 20 "ai-bot:" docker-compose.yml | grep -q "ports:"; then
        # 已有 ports 配置，添加到現有列表
        sed -i '/ai-bot:/,/^  [a-z]/ { /ports:/a \      - "3000:3000"  # Prismarine Viewer' docker-compose.yml
    else
        # 沒有 ports 配置，創建新的
        sed -i '/ai-bot:/a \    ports:\n      - "3000:3000"  # Prismarine Viewer' docker-compose.yml
    fi
fi

echo ""
echo "✅ 第一視角功能添加完成！"
echo ""
echo "📋 下一步："
echo "  1. 重啟 Docker 容器："
echo "     docker-compose down"
echo "     docker-compose up -d --build"
echo ""
echo "  2. 訪問第一視角："
echo "     http://localhost:3000"
echo ""
echo "  3. 如有問題，可從備份恢復："
echo "     cp agent_code/bot.js.backup agent_code/bot.js"
echo ""
