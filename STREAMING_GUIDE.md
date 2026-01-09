# 🎥 AI 第一視角直播指南

讓你用第一人稱視角觀看和直播 AI 玩 Minecraft！

---

## 📋 目錄

- [方案概述](#-方案概述)
- [方案一：網頁端實時視角（推薦）](#-方案一網頁端實時視角推薦)
- [方案二：Minecraft 跟隨模式](#-方案二minecraft-跟隨模式)
- [方案三：OBS 專業直播](#-方案三obs-專業直播)
- [方案四：無頭錄製](#-方案四無頭錄製)
- [直播平台設置](#-直播平台設置)

---

## 🎯 方案概述

| 方案 | 難度 | 畫質 | 延遲 | 適合場景 |
|------|------|------|------|---------|
| **Prismarine Viewer** | ⭐ | 中等 | 低 | 快速預覽、輕量直播 |
| **Minecraft 跟隨** | ⭐⭐ | 最高 | 無 | 高質量直播、錄製 |
| **OBS 直播** | ⭐⭐⭐ | 最高 | 低 | 專業直播、多平台 |
| **無頭錄製** | ⭐⭐⭐⭐ | 高 | N/A | 自動化錄製、後期剪輯 |

---

## 🌐 方案一：網頁端實時視角（推薦）

使用 **Prismarine Viewer** 在瀏覽器中渲染 AI 的第一視角。

### 優點
- ✅ 最簡單，無需額外軟體
- ✅ 可在任何設備查看（手機、平板）
- ✅ 低延遲（< 1 秒）
- ✅ 輕量化，不影響性能

### 缺點
- ⚠️ 畫質中等（WebGL 渲染）
- ⚠️ 無完整材質包支持

### 安裝步驟

#### 1. 安裝依賴

```bash
cd agent_code
npm install prismarine-viewer
```

#### 2. 修改 bot.js

```bash
# 使用提供的腳本自動添加
cd /workspaces/Project-Observer
./add_viewer.sh
```

或手動編輯 `agent_code/bot.js`：

```javascript
// 在文件頂部添加
const mineflayerViewer = require('prismarine-viewer').mineflayer;

// 在 bot.once('spawn', ...) 中添加
bot.once('spawn', () => {
    console.log('Bot spawned in game!');
    
    // 啟動第一視角查看器
    mineflayerViewer(bot, { port: 3000, firstPerson: true });
    console.log('🎥 First-person viewer started at http://localhost:3000');
    
    // ...其他代碼
});
```

#### 3. 更新 Docker Compose

編輯 `docker-compose.yml`，在 `ai-bot` 服務中添加端口映射：

```yaml
ai-bot:
  ports:
    - "3000:3000"  # 添加這一行
```

#### 4. 重啟服務

```bash
docker-compose down
docker-compose up -d --build
```

#### 5. 訪問第一視角

打開瀏覽器訪問：**http://localhost:3000**

### 控制視角

- **滑鼠拖拽**：旋轉視角
- **滾輪**：縮放
- **WASD**：移動（跟隨模式）
- **Space/Shift**：上下移動

### 直播到平台

使用 OBS 的「瀏覽器源」：

1. OBS → 添加來源 → 瀏覽器
2. URL 填入：`http://localhost:3000`
3. 寬度：1920，高度：1080
4. 開始串流！

---

## 🎮 方案二：Minecraft 跟隨模式

讓真實的 Minecraft 客戶端自動跟隨 AI，實現最高畫質。

### 優點
- ✅ 完整遊戲畫質（光影、材質包）
- ✅ 原生 Minecraft 體驗
- ✅ 可使用所有渲染特效

### 缺點
- ⚠️ 需要真實客戶端運行
- ⚠️ 消耗更多資源

### 實現方法

#### 方法 A：手動跟隨

1. 啟動 Minecraft 客戶端（Java 1.20.1）
2. 進入服務器：`localhost:25565`
3. 使用指令進入旁觀者模式：
   ```
   /gamemode spectator
   ```
4. 按 **數字鍵** 或點擊實體進入第一視角
5. 選擇 `Agent_001` 進入 AI 視角

#### 方法 B：自動跟隨插件（推薦）

創建一個跟隨機器人：

```bash
# 1. 創建跟隨腳本
cat > agent_code/follower_bot.js << 'EOF'
const mineflayer = require('mineflayer');

const follower = mineflayer.createBot({
    host: process.env.MC_HOST || 'mc-server',
    port: parseInt(process.env.MC_PORT) || 25565,
    username: 'Camera_Bot',
    version: '1.20.1'
});

follower.once('spawn', () => {
    console.log('📷 Camera bot spawned!');
    
    setInterval(() => {
        const target = follower.players['Agent_001'];
        if (target && target.entity) {
            // 跟隨 AI 的位置
            const pos = target.entity.position;
            follower.entity.position.set(pos.x, pos.y, pos.z);
            
            // 複製 AI 的視角
            const yaw = target.entity.yaw;
            const pitch = target.entity.pitch;
            follower.entity.yaw = yaw;
            follower.entity.pitch = pitch;
        }
    }, 50); // 20 FPS 更新
});

follower.on('error', console.error);
EOF

# 2. 運行跟隨機器人
node agent_code/follower_bot.js
```

然後：
1. 啟動你的 Minecraft 客戶端
2. 進入服務器
3. `/gamemode spectator`
4. 選擇 `Camera_Bot` 進入視角

### 使用 Replay Mod 錄製

安裝 [Replay Mod](https://www.replaymod.com/)：

1. 下載 Fabric 版本（1.20.1）
2. 放入 `.minecraft/mods/`
3. 進入遊戲後自動錄製
4. 後期可自由調整視角和速度

---

## 📺 方案三：OBS 專業直播

使用 OBS Studio 進行高質量直播。

### 硬體需求

- **CPU**: 6 核心以上（編碼）
- **GPU**: GTX 1660+ 或 RTX 系列（NVENC 編碼）
- **RAM**: 16GB+
- **上傳速度**: 5 Mbps+（1080p）

### 設置步驟

#### 1. 安裝 OBS Studio

```bash
# Ubuntu/Debian
sudo apt install obs-studio

# Arch Linux
sudo pacman -S obs-studio

# macOS
brew install --cask obs

# Windows
# 從 https://obsproject.com/ 下載安裝
```

#### 2. OBS 場景配置

**場景 1：遊戲主視角**
```
來源列表:
├── 遊戲捕獲 (Minecraft 客戶端)
├── 文字 (AI 當前目標)
├── 瀏覽器 (Dashboard - http://localhost:8501)
└── 圖片 (Logo/浮水印)
```

**場景 2：儀表板視圖**
```
來源列表:
├── 瀏覽器 (Dashboard - 全屏)
├── 視窗捕獲 (終端日誌)
└── 文字 (即時統計)
```

#### 3. 編碼設定

**使用 NVENC（推薦 RTX 系列）**
```
設定 → 輸出:
├── 編碼器: NVIDIA NVENC H.264
├── 速率控制: CBR
├── 位元率: 6000 Kbps (1080p) / 3500 Kbps (720p)
├── 關鍵影格間隔: 2 秒
├── 預設: Quality
└── Profile: high
```

**使用 CPU 編碼（AMD/Intel）**
```
設定 → 輸出:
├── 編碼器: x264
├── 速率控制: CBR
├── 位元率: 6000 Kbps
├── CPU 使用預設: veryfast 或 fast
└── Profile: high
```

#### 4. 直播設定

```
設定 → 串流:
├── 服務: Twitch / YouTube / 自訂
├── 伺服器: 選擇最近的
└── 串流金鑰: [你的金鑰]
```

### 進階場景：多視角

創建分割畫面：

```
布局:
┌──────────────────────────────┐
│     AI 第一視角 (大)          │
│                              │
├─────────────┬────────────────┤
│ Dashboard   │  終端日誌      │
│ (技能樹)    │  (實時輸出)    │
└─────────────┴────────────────┘
```

在 OBS 中：
1. 添加多個「瀏覽器」來源
2. 調整大小和位置
3. 使用「變換」→「編輯變換」精確對齊

---

## 🤖 方案四：無頭錄製

完全自動化的後台錄製方案，適合長時間運行。

### 使用 Prismarine Viewer + Puppeteer

#### 1. 安裝依賴

```bash
npm install puppeteer
```

#### 2. 創建錄製腳本

```bash
cat > agent_code/record_bot.js << 'EOF'
const puppeteer = require('puppeteer');
const fs = require('fs');

async function recordBot() {
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: { width: 1920, height: 1080 },
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 訪問 Prismarine Viewer
    await page.goto('http://localhost:3000');
    
    // 開始螢幕錄製
    const client = await page.target().createCDPSession();
    const { stream } = await client.send('Page.startScreencast', {
        format: 'png',
        quality: 90,
        everyNthFrame: 2 // 30 FPS (60/2)
    });
    
    let frameCount = 0;
    const outputDir = './recordings';
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);
    
    client.on('Page.screencastFrame', async ({ data, sessionId }) => {
        const buffer = Buffer.from(data, 'base64');
        fs.writeFileSync(`${outputDir}/frame_${String(frameCount).padStart(6, '0')}.png`, buffer);
        frameCount++;
        
        await client.send('Page.screencastFrameAck', { sessionId });
    });
    
    console.log('🎬 Recording started...');
    console.log('Press Ctrl+C to stop');
    
    // 錄製 1 小時後自動停止
    setTimeout(async () => {
        await client.send('Page.stopScreencast');
        await browser.close();
        console.log(`✅ Recording saved: ${frameCount} frames`);
        
        // 轉換為影片
        console.log('🎞️ Converting to video...');
        const { execSync } = require('child_process');
        execSync(`ffmpeg -framerate 30 -i ${outputDir}/frame_%06d.png -c:v libx264 -pix_fmt yuv420p output.mp4`);
        console.log('✅ Video saved: output.mp4');
    }, 3600000); // 1 小時
}

recordBot().catch(console.error);
EOF

# 3. 運行錄製
node agent_code/record_bot.js
```

### 使用 FFmpeg 直接串流

如果你有 Prismarine Viewer 運行：

```bash
#!/bin/bash
# stream_to_youtube.sh

STREAM_KEY="your-youtube-stream-key"

ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 \
    -i :0.0+0,0 \
    -f pulse -ac 2 -i default \
    -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k \
    -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 \
    -f flv rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY
```

---

## 📡 直播平台設置

### Twitch

1. 前往 https://dashboard.twitch.tv/settings/stream
2. 複製「主要串流金鑰」
3. OBS 設定：
   ```
   服務: Twitch
   伺服器: 選擇最近的 (台灣選 Hong Kong)
   串流金鑰: [貼上]
   ```

### YouTube

1. 前往 https://studio.youtube.com/
2. 點選「開始直播」→「串流」
3. 複製「串流金鑰」
4. OBS 設定：
   ```
   服務: YouTube / YouTube - RTMPS
   串流金鑰: [貼上]
   ```

### Facebook Gaming

1. 前往 https://www.facebook.com/gaming/streamer/dashboard
2. 點選「Go Live」
3. 複製「Stream Key」
4. OBS 設定：
   ```
   服務: Facebook Live
   串流金鑰: [貼上]
   ```

---

## 🎨 增強直播體驗

### 添加 AI 思維字幕

實時顯示 AI 的「內心獨白」：

```python
# overlay_thoughts.py
import time
import re
from pathlib import Path

def get_latest_thought():
    """從日誌中提取最新的 AI 決策"""
    log_dir = Path('agent_logs')
    latest_log = sorted(log_dir.glob('*.log'))[-1]
    
    with open(latest_log, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in reversed(lines):
            if 'AI Decision' in line or 'Thinking' in line:
                return line.strip()
    return "AI 思考中..."

def write_subtitle_file():
    """寫入字幕檔供 OBS 讀取"""
    while True:
        thought = get_latest_thought()
        with open('current_thought.txt', 'w', encoding='utf-8') as f:
            f.write(thought)
        time.sleep(2)

if __name__ == '__main__':
    write_subtitle_file()
```

在 OBS 中：
1. 添加「文字 (GDI+)」來源
2. 勾選「從檔案讀取」
3. 選擇 `current_thought.txt`
4. 調整字體和位置

### 添加即時統計

創建統計覆蓋層：

```python
# stats_overlay.py
import json
from pathlib import Path
from collections import Counter

def generate_stats_html():
    """生成 HTML 統計頁面"""
    skills_dir = Path('agent_skills')
    skills = list(skills_dir.glob('*.json'))
    
    total_skills = len(skills)
    success_rate = 0
    
    if skills:
        success_count = 0
        total_count = 0
        for skill_file in skills:
            with open(skill_file) as f:
                skill = json.load(f)
                success_count += skill.get('success_count', 0)
                total_count += success_count + skill.get('failure_count', 0)
        
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background: transparent;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 24px;
                padding: 20px;
            }}
            .stat {{
                background: rgba(0, 0, 0, 0.7);
                padding: 10px 20px;
                margin: 10px 0;
                border-radius: 10px;
                border-left: 4px solid #00ff00;
            }}
            .value {{
                font-size: 32px;
                font-weight: bold;
                color: #00ff00;
            }}
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <div class="stat">
            📚 學會技能: <span class="value">{total_skills}</span>
        </div>
        <div class="stat">
            ✅ 成功率: <span class="value">{success_rate:.1f}%</span>
        </div>
        <div class="stat">
            ⏱️ 運行時間: <span class="value">{get_uptime()}</span>
        </div>
    </body>
    </html>
    """
    
    with open('stats_overlay.html', 'w', encoding='utf-8') as f:
        f.write(html)

def get_uptime():
    # 實現運行時間計算
    return "2h 35m"

if __name__ == '__main__':
    import time
    while True:
        generate_stats_html()
        time.sleep(5)
```

在 OBS 中：
1. 添加「瀏覽器」來源
2. 本機檔案：`stats_overlay.html`
3. 寬度：400，高度：300
4. 放置在右上角

---

## 🎬 推薦直播布局

### 布局 1：沉浸式（單視角）

```
┌────────────────────────────────────┐
│                                    │
│        AI 第一視角 (全屏)          │
│                                    │
│                                    │
│  ┌─────────┐          ┌─────────┐ │
│  │當前目標 │          │ 統計    │ │
│  └─────────┘          └─────────┘ │
└────────────────────────────────────┘
```

### 布局 2：專業分析（多視角）

```
┌──────────────────┬─────────────────┐
│  AI 第一視角      │   Dashboard     │
│  (主要畫面)       │   (即時數據)    │
│                  │                 │
├──────────────────┼─────────────────┤
│  終端日誌         │   技能樹        │
│  (AI 思考過程)    │   (學習進度)    │
└──────────────────┴─────────────────┘
```

### 布局 3：教學模式（詳細解說）

```
┌────────────────────────────────────┐
│        AI 第一視角 (70%)           │
│                                    │
├────────────────────────────────────┤
│  即時解說字幕 (AI 正在想什麼)       │
├─────────┬─────────┬────────────────┤
│ 血量/飢餓│背包物品  │  當前技能      │
└─────────┴─────────┴────────────────┘
```

---

## ⚡ 性能優化建議

### 降低延遲

```bash
# 1. 減少日誌寫入頻率
# 編輯 agent_code/main.py
LOOP_DELAY = 2  # 從 5 降到 2

# 2. 使用更快的 AI 模型
# .env
LLM_MODEL=llama3.2:3b  # 更快的小模型

# 3. 關閉不必要的日誌
# docker-compose.yml
logging:
  driver: "none"
```

### 提升畫質

```bash
# 1. 增加 Minecraft 渲染距離
# mc-data/server.properties
view-distance=16

# 2. 使用光影包（客戶端）
# 安裝 Iris Shaders + Complementary Shaders

# 3. 提升材質解析度
# 使用 Faithful 32x 或 64x 材質包
```

### 降低資源消耗

```bash
# 1. 限制 Docker CPU 使用
docker update ai-bot --cpus="2"

# 2. 減少 Minecraft 記憶體
# docker-compose.yml
MEMORY=2G  # 從 4G 降到 2G

# 3. 使用量化模型
ollama pull llama3.1:8b-q4_0  # 量化版本
```

---

## 🆘 常見問題

### Q: Prismarine Viewer 一片黑？

**A:** 檢查：
1. bot.js 是否正確啟動 viewer
2. 端口 3000 是否被占用
3. 瀏覽器控制台是否有錯誤

```bash
# 檢查端口
netstat -tulpn | grep 3000

# 查看日誌
docker-compose logs ai-bot | grep -i viewer
```

### Q: 跟隨機器人位置不同步？

**A:** 這是因為服務器有插件限制。使用旁觀者模式更可靠：

```
/gamemode spectator @p
```

### Q: OBS 錄製卡頓？

**A:** 優化設定：
1. 降低輸出解析度到 720p
2. 使用 GPU 編碼（NVENC）
3. 降低遊戲畫質設定
4. 關閉其他應用程式

### Q: 直播有延遲？

**A:** 
- **Twitch**: 延遲 3-5 秒（正常）
- **YouTube**: 延遲 10-20 秒（正常）
- 使用「低延遲模式」可減少到 1-2 秒

---

## 🎯 完整工作流程範例

### 場景：24 小時 Twitch 直播

```bash
#!/bin/bash
# start_stream.sh

# 1. 啟動系統
./start.sh

# 2. 等待啟動完成
sleep 30

# 3. 啟動 Prismarine Viewer
cd agent_code
npm install prismarine-viewer
node bot.js &

# 4. 啟動統計覆蓋層
python3 stats_overlay.py &

# 5. 啟動思維字幕
python3 overlay_thoughts.py &

# 6. 打開 OBS（需手動設定場景）
obs &

# 7. 監控日誌
./logs.sh

echo "✅ 直播環境已就緒！"
echo "📺 請在 OBS 中點擊「開始串流」"
```

---

## 📚 延伸資源

- [Prismarine Viewer 文檔](https://github.com/PrismarineJS/prismarine-viewer)
- [OBS Studio 教學](https://obsproject.com/wiki/)
- [Replay Mod 官網](https://www.replaymod.com/)
- [FFmpeg 串流指南](https://trac.ffmpeg.org/wiki/StreamingGuide)

---

**開始你的 AI 直播之旅吧！🎥✨**
