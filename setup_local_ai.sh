#!/bin/bash

# Project Observer - 本地 AI 一鍵設置腳本
# 完全不需要 OpenAI API

echo "🧠 Project Observer - 本地 AI 設置"
echo "===================================="
echo ""

# 檢查 Ollama 是否已安裝
if command -v ollama &> /dev/null; then
    echo "✅ Ollama 已安裝"
    ollama --version
else
    echo "📦 安裝 Ollama..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "請從以下網址下載 Ollama for macOS:"
        echo "https://ollama.com/download/mac"
        exit 1
    else
        echo "❌ 不支持的操作系統: $OSTYPE"
        echo "請手動安裝 Ollama: https://ollama.com"
        exit 1
    fi
fi

echo ""
echo "🔍 選擇要使用的模型:"
echo "  1) Llama 3.1 8B    - 推薦，平衡性能 (4.7GB)"
echo "  2) Llama 3.2 3B    - 更快，適合低配置 (2GB)"
echo "  3) Mistral 7B      - 高質量輸出 (4.1GB)"
echo "  4) Qwen 2.5 7B     - 中文優化 (4.4GB)"
echo "  5) Phi-3 Mini      - 超輕量級 (2.3GB)"
echo ""

read -p "請選擇 (1-5，默認 1): " model_choice
model_choice=${model_choice:-1}

case $model_choice in
    1)
        MODEL="llama3.1:8b"
        MODEL_SIZE="4.7GB"
        ;;
    2)
        MODEL="llama3.2:3b"
        MODEL_SIZE="2GB"
        ;;
    3)
        MODEL="mistral:7b"
        MODEL_SIZE="4.1GB"
        ;;
    4)
        MODEL="qwen2.5:7b"
        MODEL_SIZE="4.4GB"
        ;;
    5)
        MODEL="phi3:mini"
        MODEL_SIZE="2.3GB"
        ;;
    *)
        echo "❌ 無效選項，使用默認模型"
        MODEL="llama3.1:8b"
        MODEL_SIZE="4.7GB"
        ;;
esac

echo ""
echo "📥 下載模型: $MODEL ($MODEL_SIZE)"
echo "   這可能需要幾分鐘時間..."
echo ""

ollama pull $MODEL

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 模型下載完成！"
else
    echo "❌ 模型下載失敗"
    exit 1
fi

# 啟動 Ollama 服務
echo ""
echo "🚀 啟動 Ollama 服務..."

# 檢查是否已經在運行
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama 服務已在運行"
else
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
    echo "✅ Ollama 服務已啟動"
fi

# 配置 .env 文件
echo ""
echo "⚙️  配置 Project Observer..."

if [ ! -f .env ]; then
    cp .env.example .env
fi

# 更新 .env 文件
cat > .env << EOF
# ========================================
# 本地 AI 配置 (使用 Ollama)
# ========================================

OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=$MODEL
OPENAI_API_KEY=ollama

# LLM 參數
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
LLM_NUM_CTX=4096

# Agent 配置
BOT_USERNAME=Agent_001
LOG_LEVEL=INFO

# Minecraft 配置
MC_VERSION=1.20.1
MC_DIFFICULTY=normal
MC_MAX_MEMORY=2G
EOF

echo "✅ 配置文件已更新"

# 測試模型
echo ""
echo "🧪 測試模型..."
echo ""

TEST_RESPONSE=$(ollama run $MODEL "你是一個 Minecraft AI。看到樹林，你會做什麼？" | head -n 3)

if [ ! -z "$TEST_RESPONSE" ]; then
    echo "✅ 模型測試成功！"
    echo ""
    echo "模型回應:"
    echo "$TEST_RESPONSE"
else
    echo "⚠️  模型測試未返回結果，但可能仍然可用"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 本地 AI 設置完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 配置摘要:"
echo "  • 模型: $MODEL"
echo "  • API 地址: http://host.docker.internal:11434"
echo "  • 無需 OpenAI API Key"
echo ""
echo "🚀 下一步:"
echo "  1. 啟動系統: ./start.sh 或 make start"
echo "  2. 訪問 Dashboard: http://localhost:8501"
echo "  3. 觀察 AI 使用本地模型進行思考"
echo ""
echo "📖 更多信息: cat LOCAL_AI_GUIDE.md"
echo ""
echo "💡 提示:"
echo "  • 查看 Ollama 日誌: tail -f ollama.log"
echo "  • 測試模型: ollama run $MODEL"
echo "  • 下載更多模型: ollama pull <model>"
echo ""
