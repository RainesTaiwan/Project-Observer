# 🧠 本地 AI 訓練指南 - 不使用 OpenAI

本指南將教你如何使用本地 AI 模型運行 Project Observer，完全不依賴 OpenAI API。

## 目錄
- [為什麼使用本地 AI](#為什麼使用本地-ai)
- [選擇本地模型](#選擇本地模型)
- [Ollama 快速設置](#ollama-快速設置)
- [進階：訓練自己的模型](#進階訓練自己的模型)
- [性能優化](#性能優化)
- [故障排除](#故障排除)

---

## 為什麼使用本地 AI

✅ **優勢**：
- 💰 **完全免費** - 無需支付 API 費用
- 🔒 **數據隱私** - 所有數據保留在本地
- ⚡ **無限調用** - 沒有速率限制
- 🎯 **可定制** - 可以微調專屬模型
- 🌐 **離線運行** - 不需要網路連接

⚠️ **考量**：
- 需要較高的硬體配置（GPU 推薦）
- 初次下載模型需要時間
- 推理速度可能較慢（取決於硬體）

---

## 選擇本地模型

### 推薦模型（按性能排序）

| 模型 | 參數量 | 記憶體需求 | 推薦用途 | 下載大小 |
|------|--------|-----------|---------|----------|
| **Llama 3.1 70B** | 70B | 48GB+ | 最佳性能 | 40GB |
| **Llama 3.1 8B** | 8B | 8GB | 平衡選擇 | 4.7GB |
| **Llama 3.2 3B** | 3B | 4GB | 快速推理 | 2GB |
| **Phi-3 Mini** | 3.8B | 4GB | 輕量級 | 2.3GB |
| **Mistral 7B** | 7B | 8GB | 高質量 | 4.1GB |
| **Qwen 2.5** | 7B | 8GB | 中文優化 | 4.4GB |

### 硬體需求對照

- **基礎配置**：8GB RAM + CPU → Llama 3.2 3B
- **推薦配置**：16GB RAM + RTX 3060 → Llama 3.1 8B
- **高階配置**：32GB RAM + RTX 4090 → Llama 3.1 70B

---

## Ollama 快速設置

### 1. 安裝 Ollama

#### Linux / macOS
```bash
# 一鍵安裝
curl -fsSL https://ollama.com/install.sh | sh

# 驗證安裝
ollama --version
```

#### Windows
```powershell
# 下載並安裝 Ollama for Windows
# https://ollama.com/download/windows

# 或使用 WSL2
wsl -d Ubuntu
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. 下載模型

```bash
# 推薦：Llama 3.1 8B (平衡性能和速度)
ollama pull llama3.1:8b

# 或選擇其他模型
ollama pull llama3.2:3b      # 更快，較小
ollama pull mistral:7b       # 高質量
ollama pull qwen2.5:7b       # 中文友好
ollama pull phi3:mini        # 輕量級
```

### 3. 啟動 Ollama 服務

```bash
# 前台運行（查看日誌）
ollama serve

# 或背景運行
nohup ollama serve > ollama.log 2>&1 &
```

### 4. 測試模型

```bash
# 交互式測試
ollama run llama3.1:8b

# 測試提示
ollama run llama3.1:8b "你是一個在 Minecraft 世界中生存的 AI。現在你看到前方有一棵樹，你應該做什麼？"
```

### 5. 配置 Project Observer

編輯 `.env` 文件：

```bash
# 停用 OpenAI
# OPENAI_API_KEY=sk-xxxxx

# 啟用本地 Ollama
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.1:8b
OPENAI_API_KEY=ollama  # 任意值即可

# 可選：調整推理參數
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

### 6. 啟動系統

```bash
# 確保 Ollama 正在運行
ollama serve &

# 啟動 Project Observer
make start

# 查看日誌確認使用本地模型
make logs-ai | grep "LLM"
```

---

## 進階：訓練自己的模型

### 方法一：使用 Ollama Modelfile 自定義

創建專屬的 Minecraft AI 模型：

```bash
# 1. 創建 Modelfile
cat > MinecraftAgent.modelfile << 'EOF'
FROM llama3.1:8b

# 設置系統提示詞
SYSTEM """
你是一個專業的 Minecraft 生存專家 AI。你的目標是：
1. 高效地收集資源
2. 建造安全的庇護所
3. 製作進階工具和裝備
4. 探索並征服不同的生物群系

你總是用 JSON 格式回應，包含清晰的目標、推理和代碼。
你從錯誤中快速學習，並不斷優化策略。
"""

# 調整參數
PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096

# 添加範例對話
MESSAGE user 我看到前方有樹林，背包是空的。
MESSAGE assistant {"goal": "獲取木頭製作工具", "reasoning": "木頭是最基礎的資源，可以製作工作台和木製工具", "action_type": "generate_code", "code": "await bot.pathfinder.goto(new goals.GoalNear(treePosition.x, treePosition.y, treePosition.z, 1)); await mineBlock('oak_log');"}

MESSAGE user 我的血量只剩 5 點，附近有殭屍。
MESSAGE assistant {"goal": "逃離危險區域", "reasoning": "低血量時應避免戰鬥，優先生存", "action_type": "generate_code", "code": "const safeDistance = 50; await bot.pathfinder.goto(new goals.GoalInvert(new goals.GoalFollow(zombie, safeDistance)));"}
EOF

# 2. 創建自定義模型
ollama create minecraft-agent -f MinecraftAgent.modelfile

# 3. 測試模型
ollama run minecraft-agent "我在沙漠中，口渴且飢餓。"

# 4. 使用自定義模型
# 修改 .env
LLM_MODEL=minecraft-agent
```

### 方法二：使用真實遊戲數據微調

#### 準備訓練數據

```bash
# 創建訓練數據目錄
mkdir -p training_data

# 收集 AI 的成功案例
cat > training_data/minecraft_examples.jsonl << 'EOF'
{"prompt": "觀察：生命值20，飢餓值15，周圍有橡樹。目標是什麼？", "response": "收集木頭是首要任務。木頭可以製作工作台和工具。", "code": "await mineBlock('oak_log');"}
{"prompt": "觀察：夜晚，血量10，附近有3隻殭屍。策略？", "response": "夜晚且低血量應避免戰鬥，尋找高處或建造臨時庇護所。", "code": "await bot.placeBlock(bot.blockAt(bot.entity.position.offset(0, -1, 1)), new Vec3(0, 1, 0));"}
{"prompt": "觀察：有工作台和木頭，需要更好的工具。", "response": "製作木鎬，然後挖石頭升級到石製工具。", "code": "await bot.craft(mcData.itemsByName['wooden_pickaxe'], 1);"}
EOF
```

#### 使用 LLaMA Factory 微調

```bash
# 1. 安裝 LLaMA Factory
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e .

# 2. 準備配置
cat > minecraft_lora_config.yaml << 'EOF'
model_name_or_path: meta-llama/Llama-3.1-8B
stage: sft
do_train: true
finetuning_type: lora
lora_target: all

dataset: minecraft_survival
template: llama3
cutoff_len: 2048
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 16

output_dir: minecraft_agent_lora
logging_steps: 10
save_steps: 100
plot_loss: true

per_device_train_batch_size: 2
gradient_accumulation_steps: 8
learning_rate: 5.0e-5
num_train_epochs: 3.0

lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
EOF

# 3. 開始訓練
llamafactory-cli train minecraft_lora_config.yaml

# 4. 合併 LoRA 權重
llamafactory-cli export \
  --model_name_or_path meta-llama/Llama-3.1-8B \
  --adapter_name_or_path minecraft_agent_lora \
  --export_dir minecraft_agent_merged

# 5. 轉換為 Ollama 格式
ollama create minecraft-agent-trained \
  -f <(echo "FROM ./minecraft_agent_merged")
```

### 方法三：使用強化學習（高階）

```python
# rl_trainer.py - 強化學習訓練腳本
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback

class MinecraftAgentEnv(gym.Env):
    """自定義 Minecraft 環境"""
    def __init__(self):
        super().__init__()
        # 定義動作空間（挖掘、移動、製作等）
        self.action_space = gym.spaces.Discrete(10)
        # 定義觀察空間（周圍方塊、生命值等）
        self.observation_space = gym.spaces.Box(...)
    
    def step(self, action):
        # 執行動作，返回獎勵
        reward = self.calculate_reward(action)
        return obs, reward, done, info
    
    def calculate_reward(self, action):
        # 獎勵函數設計
        reward = 0
        if action == "collect_wood":
            reward += 10
        if agent.health > 15:
            reward += 5
        if agent.has_shelter:
            reward += 20
        return reward

# 創建環境並訓練
env = MinecraftAgentEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)
model.save("minecraft_rl_agent")
```

---

## 性能優化

### 1. 使用量化模型（更快推理）

```bash
# 下載 4-bit 量化版本（更快，較小）
ollama pull llama3.1:8b-q4_0

# 或 8-bit 量化（質量更好）
ollama pull llama3.1:8b-q8_0

# 更新 .env
LLM_MODEL=llama3.1:8b-q4_0
```

### 2. GPU 加速

```bash
# 檢查 GPU 支持
nvidia-smi

# Ollama 會自動使用 GPU
# 查看 GPU 使用情況
watch -n 1 nvidia-smi
```

### 3. 調整並行參數

編輯 `.env`：
```bash
# 減少並行請求（避免 OOM）
LLM_NUM_PARALLEL=1

# 調整上下文窗口
LLM_NUM_CTX=4096

# 調整批次大小
LLM_BATCH_SIZE=512
```

### 4. 使用更快的採樣策略

```bash
# 創建快速推理配置
cat > FastAgent.modelfile << 'EOF'
FROM llama3.1:8b-q4_0

PARAMETER temperature 0.5
PARAMETER top_p 0.8
PARAMETER num_predict 200
PARAMETER stop "<|eot_id|>"
EOF

ollama create fast-agent -f FastAgent.modelfile
```

---

## 故障排除

### 問題 1: Ollama 無法啟動

```bash
# 檢查端口佔用
lsof -i :11434

# 查看詳細錯誤
ollama serve --debug

# 重置 Ollama
rm -rf ~/.ollama
ollama pull llama3.1:8b
```

### 問題 2: Docker 無法連接 Ollama

```bash
# 確認 host.docker.internal 可用
docker run --rm alpine ping -c 3 host.docker.internal

# 或使用宿主機 IP
ip addr show docker0 | grep inet
# 修改 .env
OPENAI_API_BASE=http://172.17.0.1:11434/v1
```

### 問題 3: 模型推理太慢

```bash
# 1. 使用更小的模型
ollama pull llama3.2:3b

# 2. 使用量化版本
ollama pull llama3.1:8b-q4_0

# 3. 增加 GPU 記憶體
export OLLAMA_GPU_MEMORY=8GB

# 4. 減少上下文長度
# 在 .env 中設置
LLM_NUM_CTX=2048
```

### 問題 4: 記憶體不足

```bash
# 監控記憶體使用
watch -n 1 free -h

# 使用更小的模型
ollama pull phi3:mini

# 或限制 Ollama 記憶體
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1
```

---

## 模型比較測試

創建測試腳本來比較不同模型：

```bash
# test_models.sh
#!/bin/bash

MODELS=("llama3.1:8b" "mistral:7b" "qwen2.5:7b" "phi3:mini")

for model in "${MODELS[@]}"; do
    echo "測試模型: $model"
    time ollama run $model "我在 Minecraft 中，看到遠處有村莊。我應該做什麼？" \
        | head -n 20
    echo "---"
done
```

---

## 生產環境部署

### 使用 Ollama 伺服器模式

```yaml
# docker-compose.override.yml
version: "3.8"

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-server
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    environment:
      - OLLAMA_NUM_PARALLEL=2
      - OLLAMA_MAX_LOADED_MODELS=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - ai-net
  
  ai-bot:
    depends_on:
      - ollama
    environment:
      OPENAI_API_BASE: http://ollama:11434/v1
      LLM_MODEL: llama3.1:8b

volumes:
  ollama-data:
```

啟動：
```bash
# 下載模型到 Ollama 容器
docker-compose exec ollama ollama pull llama3.1:8b

# 重啟 AI Agent
docker-compose restart ai-bot
```

---

## 推薦配置方案

### 方案 A：入門級（8GB RAM，無 GPU）
```bash
# .env
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=phi3:mini
LLM_NUM_CTX=2048
LLM_TEMPERATURE=0.7
```

### 方案 B：標準級（16GB RAM + RTX 3060）
```bash
# .env
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.1:8b-q4_0
LLM_NUM_CTX=4096
LLM_TEMPERATURE=0.8
```

### 方案 C：專業級（32GB+ RAM + RTX 4090）
```bash
# .env
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.1:70b
LLM_NUM_CTX=8192
LLM_TEMPERATURE=0.9
```

---

## 下一步

1. ✅ 安裝 Ollama
2. ✅ 下載適合的模型
3. ✅ 配置 Project Observer
4. ✅ 測試本地 AI
5. 📈 收集數據準備微調
6. 🎯 訓練專屬模型

完全擺脫 OpenAI，擁有自己的 Minecraft AI！🚀

---

## 參考資源

- [Ollama 官方文檔](https://ollama.com/docs)
- [LLaMA Factory](https://github.com/hiyouga/LLaMA-Factory)
- [Hugging Face 模型庫](https://huggingface.co/models)
- [Stable Baselines3](https://stable-baselines3.readthedocs.io/)
