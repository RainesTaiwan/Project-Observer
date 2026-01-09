# 🚀 Project Observer - 部署指南

完整的生產環境部署文檔，從本地測試到雲端部署。

---

## 📋 目錄

- [部署選項概覽](#-部署選項概覽)
- [環境準備](#-環境準備)
- [本地部署](#-本地部署)
- [VPS/雲端部署](#-vps雲端部署)
- [Docker Swarm 集群部署](#-docker-swarm-集群部署)
- [Kubernetes 部署](#-kubernetes-部署)
- [安全性配置](#-安全性配置)
- [監控與維護](#-監控與維護)
- [備份與恢復](#-備份與恢復)
- [故障排除](#-故障排除)

---

## 🎯 部署選項概覽

| 部署方式 | 難度 | 成本 | 適用場景 | 推薦度 |
|---------|------|------|---------|--------|
| **本地 Docker** | ⭐ | 免費 | 開發測試 | ⭐⭐⭐⭐⭐ |
| **單一 VPS** | ⭐⭐ | $5-20/月 | 個人使用、小型展示 | ⭐⭐⭐⭐ |
| **AWS/GCP** | ⭐⭐⭐ | $20-100/月 | 生產環境、高可用 | ⭐⭐⭐⭐ |
| **Docker Swarm** | ⭐⭐⭐ | $30+/月 | 多機分佈式 | ⭐⭐⭐ |
| **Kubernetes** | ⭐⭐⭐⭐⭐ | $50+/月 | 企業級、超大規模 | ⭐⭐ |

---

## 🛠️ 環境準備

### 系統需求

#### 最低要求（開發/測試）
```yaml
CPU: 4 核心
RAM: 8GB
儲存: 20GB SSD
OS: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
Docker: 20.10+
Docker Compose: 2.0+
```

#### 推薦配置（生產環境）
```yaml
CPU: 6+ 核心
RAM: 16GB+
儲存: 50GB+ SSD
OS: Ubuntu 22.04 LTS
Docker: 最新穩定版
Docker Compose: 最新穩定版
防火牆: UFW / iptables
反向代理: Nginx / Traefik
SSL 證書: Let's Encrypt
```

### 必要軟體安裝

```bash
#!/bin/bash
# install_dependencies.sh

set -e

echo "🔧 安裝系統依賴..."

# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝基礎工具
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    vim \
    htop \
    ufw

# 安裝 Docker
echo "🐳 安裝 Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安裝 Docker Compose
echo "📦 安裝 Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 啟動 Docker
sudo systemctl enable docker
sudo systemctl start docker

echo "✅ 依賴安裝完成！"
echo "⚠️  請登出並重新登入以使 Docker 權限生效"
```

---

## 💻 本地部署

### 快速啟動（開發模式）

```bash
# 1. Clone 專案
git clone https://github.com/RainesTaiwan/Project-Observer.git
cd Project-Observer

# 2. 配置環境變數
cp .env.example .env
nano .env

# 3. 啟動所有服務
docker-compose up -d

# 4. 查看日誌
docker-compose logs -f

# 5. 訪問服務
# Dashboard: http://localhost:8501
# Minecraft: localhost:25565
# ChromaDB: http://localhost:8000
```

### 使用本地 AI（推薦）

```bash
# 自動安裝 Ollama
./setup_local_ai.sh

# 或手動配置
ollama pull llama3.1:8b

# 修改 .env
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.1:8b
OPENAI_API_KEY=ollama
```

---

## 🌐 VPS/雲端部署

### 步驟 1：選擇 VPS 提供商

推薦選項：

#### DigitalOcean Droplet
```yaml
配置: Basic Droplet
規格: 4 vCPU, 8GB RAM
儲存: 160GB SSD
價格: $48/月
地區: Singapore / San Francisco
```

#### AWS EC2
```yaml
實例: t3.large
規格: 2 vCPU, 8GB RAM
儲存: EBS 50GB
價格: ~$60/月
地區: ap-northeast-1 (東京)
```

#### Google Cloud Platform
```yaml
機器類型: e2-standard-2
規格: 2 vCPU, 8GB RAM
儲存: 50GB SSD
價格: ~$50/月
地區: asia-east1 (台灣)
```

#### Linode
```yaml
配置: Dedicated 8GB
規格: 4 vCPU, 8GB RAM
儲存: 160GB SSD
價格: $36/月
地區: Tokyo
```

### 步驟 2：初始化 VPS

```bash
# SSH 連接到 VPS
ssh root@your_server_ip

# 創建新用戶（安全性）
adduser minecraft
usermod -aG sudo minecraft
usermod -aG docker minecraft

# 配置 SSH 金鑰登入（推薦）
mkdir -p /home/minecraft/.ssh
cp ~/.ssh/authorized_keys /home/minecraft/.ssh/
chown -R minecraft:minecraft /home/minecraft/.ssh
chmod 700 /home/minecraft/.ssh
chmod 600 /home/minecraft/.ssh/authorized_keys

# 禁用 root SSH 登入
nano /etc/ssh/sshd_config
# 設置: PermitRootLogin no
sudo systemctl restart sshd

# 配置防火牆
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 25565/tcp   # Minecraft
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

### 步驟 3：安裝依賴

```bash
# 切換到普通用戶
su - minecraft

# 安裝 Docker
curl -fsSL https://get.docker.com | sh

# 安裝 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 驗證安裝
docker --version
docker-compose --version
```

### 步驟 4：部署專案

```bash
# Clone 專案
cd ~
git clone https://github.com/RainesTaiwan/Project-Observer.git
cd Project-Observer

# 配置環境
cp .env.example .env
nano .env

# 生產環境配置建議
cat > .env << 'EOF'
# AI 配置（使用本地 Ollama）
OPENAI_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=llama3.1:8b
OPENAI_API_KEY=ollama

# Minecraft 配置
MC_HOST=mc-server
MC_PORT=25565
BOT_USERNAME=AI_Agent

# ChromaDB 配置
CHROMA_HOST=chromadb
CHROMA_PORT=8000

# 日誌等級（生產環境建議 INFO）
LOG_LEVEL=INFO

# Dashboard 配置
DASHBOARD_PORT=8501
EOF

# 安裝本地 AI（推薦）
./setup_local_ai.sh

# 啟動服務（生產模式）
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 查看狀態
docker-compose ps
```

### 步驟 5：配置反向代理（Nginx）

```bash
# 安裝 Nginx
sudo apt install nginx -y

# 配置站點
sudo nano /etc/nginx/sites-available/project-observer

# 貼上配置
cat > /tmp/nginx-config << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    # Streamlit Dashboard
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_read_timeout 86400;
    }
    
    # First-person Viewer
    location /viewer {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
    
    # ChromaDB API (可選，不建議公開)
    # location /api/chroma {
    #     proxy_pass http://localhost:8000;
    #     proxy_set_header Host $host;
    # }
}
EOF

sudo mv /tmp/nginx-config /etc/nginx/sites-available/project-observer

# 啟用站點
sudo ln -s /etc/nginx/sites-available/project-observer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 步驟 6：配置 SSL（Let's Encrypt）

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 獲取 SSL 證書
sudo certbot --nginx -d your-domain.com

# 自動續期測試
sudo certbot renew --dry-run

# 現在可以通過 HTTPS 訪問
# https://your-domain.com
```

---

## 🚢 Docker Swarm 集群部署

適合多伺服器分佈式部署。

### 架構設計

```
┌─────────────────────────────────────────┐
│           Manager Node (主節點)          │
│   - Docker Swarm Manager                │
│   - Nginx Load Balancer                 │
│   - Monitoring (Prometheus/Grafana)     │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│ Worker Node 1│        │ Worker Node 2│
│ - Minecraft  │        │ - AI Agent   │
│ - ChromaDB   │        │ - Dashboard  │
└──────────────┘        └──────────────┘
```

### 初始化 Swarm

```bash
# 在 Manager Node
docker swarm init --advertise-addr <MANAGER-IP>

# 輸出會顯示 join token
# docker swarm join --token SWMTKN-xxx <MANAGER-IP>:2377

# 在 Worker Nodes 執行 join 命令
docker swarm join --token SWMTKN-xxx <MANAGER-IP>:2377

# 驗證集群
docker node ls
```

### 創建 Stack 配置

```yaml
# docker-stack.yml
version: '3.8'

services:
  mc-server:
    image: itzg/minecraft-server:latest
    environment:
      EULA: "TRUE"
      TYPE: "FABRIC"
      VERSION: "1.20.1"
      MEMORY: 4G
    volumes:
      - mc-data:/data
    ports:
      - "25565:25565"
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == worker
      resources:
        limits:
          cpus: '2'
          memory: 4G

  chromadb:
    image: chromadb/chroma:latest
    volumes:
      - chroma-data:/chroma/chroma
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == worker

  ai-bot:
    image: project-observer-ai-bot:latest
    depends_on:
      - mc-server
      - chromadb
    volumes:
      - agent-skills:/app/skills
      - agent-logs:/app/logs
    deploy:
      replicas: 2  # 可運行多個 AI
      restart_policy:
        condition: on-failure

  dashboard:
    image: project-observer-dashboard:latest
    ports:
      - "8501:8501"
    deploy:
      replicas: 1

volumes:
  mc-data:
  chroma-data:
  agent-skills:
  agent-logs:

networks:
  default:
    driver: overlay
```

### 部署 Stack

```bash
# 構建並推送鏡像到私有 Registry
docker-compose build
docker tag project-observer-ai-bot:latest registry.example.com/ai-bot:latest
docker push registry.example.com/ai-bot:latest

# 部署 Stack
docker stack deploy -c docker-stack.yml observer

# 查看服務
docker stack services observer
docker service logs observer_ai-bot
```

---

## ☸️ Kubernetes 部署

適合企業級大規模部署。

### Helm Chart

```yaml
# values.yaml
replicaCount:
  aiBot: 3
  dashboard: 2
  minecraft: 1
  chromadb: 1

image:
  aiBot:
    repository: your-registry/ai-bot
    tag: latest
  dashboard:
    repository: your-registry/dashboard
    tag: latest

resources:
  aiBot:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 512Mi

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: observer.example.com
      paths:
        - path: /
          pathType: Prefix

persistence:
  minecraft:
    size: 20Gi
    storageClassName: fast-ssd
  chromadb:
    size: 10Gi
  skills:
    size: 5Gi
```

### 部署命令

```bash
# 添加 Helm Repository（如果打包了）
helm repo add observer https://charts.example.com/observer

# 部署
helm install my-observer observer/project-observer \
  --namespace observer \
  --create-namespace \
  -f values.yaml

# 升級
helm upgrade my-observer observer/project-observer \
  -f values.yaml

# 查看狀態
kubectl get pods -n observer
kubectl logs -n observer deployment/ai-bot
```

---

## 🔒 安全性配置

### 1. 環境變數加密

```bash
# 使用 Docker Secrets
echo "your-api-key" | docker secret create openai_key -

# 在 docker-compose 中使用
services:
  ai-bot:
    secrets:
      - openai_key
    environment:
      OPENAI_API_KEY_FILE: /run/secrets/openai_key

secrets:
  openai_key:
    external: true
```

### 2. 網路隔離

```yaml
# docker-compose.prod.yml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 無外網訪問

services:
  dashboard:
    networks:
      - frontend
  
  ai-bot:
    networks:
      - frontend
      - backend
  
  chromadb:
    networks:
      - backend  # 僅內部訪問
```

### 3. 限制資源

```yaml
services:
  ai-bot:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 4. 日誌脫敏

```python
# 在 Python 代碼中
import re

def sanitize_log(message):
    """移除敏感信息"""
    # 隱藏 API Keys
    message = re.sub(r'sk-[a-zA-Z0-9]{32,}', 'sk-****', message)
    # 隱藏 IP 地址
    message = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '***.***.***', message)
    return message
```

---

## 📊 監控與維護

### Prometheus + Grafana

```yaml
# monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana
    volumes:
      - grafana-data:/var/lib/grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro

volumes:
  prometheus-data:
  grafana-data:
```

### 健康檢查腳本

```bash
#!/bin/bash
# health_check.sh

set -e

echo "🏥 執行健康檢查..."

# 檢查 Docker 容器
containers=("mc-server" "chromadb" "ai-bot" "dashboard")
for container in "${containers[@]}"; do
    if docker ps | grep -q $container; then
        echo "✅ $container: 運行中"
    else
        echo "❌ $container: 已停止"
        docker-compose restart $container
    fi
done

# 檢查端口
ports=(25565 8000 8501)
for port in "${ports[@]}"; do
    if netstat -tuln | grep -q ":$port "; then
        echo "✅ Port $port: 開放"
    else
        echo "❌ Port $port: 未開放"
    fi
done

# 檢查磁碟空間
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $disk_usage -gt 80 ]; then
    echo "⚠️  磁碟使用率: ${disk_usage}% (建議清理)"
else
    echo "✅ 磁碟使用率: ${disk_usage}%"
fi

# 檢查記憶體
mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
echo "📊 記憶體使用率: ${mem_usage}%"

echo "✅ 健康檢查完成"
```

### 自動化維護

```bash
# /etc/cron.d/project-observer

# 每天凌晨 3 點備份
0 3 * * * minecraft /home/minecraft/Project-Observer/backup.sh

# 每小時執行健康檢查
0 * * * * minecraft /home/minecraft/Project-Observer/health_check.sh

# 每週日清理日誌
0 2 * * 0 minecraft docker system prune -af --volumes
```

---

## 💾 備份與恢復

### 自動備份腳本

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/project-observer"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$DATE"

mkdir -p $BACKUP_PATH

echo "🔄 開始備份..."

# 1. 停止容器（可選）
# docker-compose stop

# 2. 備份 Minecraft 世界
echo "📦 備份 Minecraft 世界..."
docker run --rm \
    -v project-observer_mc-data:/data \
    -v $BACKUP_PATH:/backup \
    alpine tar czf /backup/minecraft-world.tar.gz /data

# 3. 備份 ChromaDB
echo "📦 備份 ChromaDB..."
docker run --rm \
    -v project-observer_chroma-data:/chroma \
    -v $BACKUP_PATH:/backup \
    alpine tar czf /backup/chromadb.tar.gz /chroma

# 4. 備份技能
echo "📦 備份技能庫..."
docker run --rm \
    -v project-observer_agent-skills:/skills \
    -v $BACKUP_PATH:/backup \
    alpine tar czf /backup/skills.tar.gz /skills

# 5. 備份配置
echo "📦 備份配置文件..."
cp .env $BACKUP_PATH/
cp docker-compose.yml $BACKUP_PATH/

# 6. 重啟容器
# docker-compose start

# 7. 清理舊備份（保留 7 天）
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} +

echo "✅ 備份完成: $BACKUP_PATH"

# 8. 上傳到雲端（可選）
# rclone copy $BACKUP_PATH remote:backups/
```

### 恢復流程

```bash
#!/bin/bash
# restore.sh

BACKUP_PATH=$1

if [ -z "$BACKUP_PATH" ]; then
    echo "使用方式: ./restore.sh /path/to/backup"
    exit 1
fi

echo "🔄 開始恢復..."

# 1. 停止所有容器
docker-compose down

# 2. 恢復數據
docker run --rm \
    -v project-observer_mc-data:/data \
    -v $BACKUP_PATH:/backup \
    alpine tar xzf /backup/minecraft-world.tar.gz -C /

docker run --rm \
    -v project-observer_chroma-data:/chroma \
    -v $BACKUP_PATH:/backup \
    alpine tar xzf /backup/chromadb.tar.gz -C /

docker run --rm \
    -v project-observer_agent-skills:/skills \
    -v $BACKUP_PATH:/backup \
    alpine tar xzf /backup/skills.tar.gz -C /

# 3. 恢復配置
cp $BACKUP_PATH/.env .env
cp $BACKUP_PATH/docker-compose.yml docker-compose.yml

# 4. 重啟服務
docker-compose up -d

echo "✅ 恢復完成"
```

---

## 🆘 故障排除

### 常見問題

#### 1. 容器無法啟動

```bash
# 查看詳細錯誤
docker-compose logs <service-name>

# 檢查資源使用
docker stats

# 重建容器
docker-compose down
docker-compose up -d --build
```

#### 2. Minecraft 連接失敗

```bash
# 檢查端口
sudo netstat -tuln | grep 25565

# 檢查防火牆
sudo ufw status
sudo ufw allow 25565/tcp

# 檢查服務器日誌
docker-compose logs mc-server | tail -100
```

#### 3. AI Bot 不回應

```bash
# 檢查 LLM API
curl http://localhost:11434/v1/models  # Ollama

# 檢查環境變數
docker-compose exec ai-bot env | grep OPENAI

# 重啟 AI Bot
docker-compose restart ai-bot
```

#### 4. Dashboard 無法訪問

```bash
# 檢查端口衝突
sudo lsof -i :8501

# 檢查 Nginx 配置
sudo nginx -t
sudo systemctl status nginx

# 查看 Dashboard 日誌
docker-compose logs dashboard
```

#### 5. 記憶體不足

```bash
# 清理未使用的資源
docker system prune -a

# 限制容器記憶體
# docker-compose.yml
services:
  mc-server:
    mem_limit: 4g

# 增加 swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📝 生產環境檢查清單

### 部署前

- [ ] 已選擇適合的 VPS/雲端服務
- [ ] 已配置 SSH 金鑰登入
- [ ] 已安裝所有依賴（Docker, Docker Compose）
- [ ] 已配置防火牆規則
- [ ] 已準備域名並設置 DNS
- [ ] 已配置環境變數（`.env`）
- [ ] 已選擇 LLM（OpenAI 或本地 Ollama）

### 安全性

- [ ] 禁用 root SSH 登入
- [ ] 配置防火牆（UFW）
- [ ] 使用 Docker Secrets 管理敏感信息
- [ ] 配置網路隔離
- [ ] 設置資源限制
- [ ] 啟用 SSL/TLS（Let's Encrypt）

### 監控

- [ ] 設置健康檢查
- [ ] 配置日誌輪替
- [ ] 部署監控系統（Prometheus/Grafana）
- [ ] 設置告警通知
- [ ] 配置性能監控

### 備份

- [ ] 設置自動備份腳本
- [ ] 測試恢復流程
- [ ] 配置異地備份
- [ ] 設置備份保留策略

### 部署後

- [ ] 驗證所有服務正常運行
- [ ] 測試 Minecraft 連接
- [ ] 測試 Dashboard 訪問
- [ ] 測試 AI Bot 功能
- [ ] 驗證 SSL 證書
- [ ] 檢查日誌輪替
- [ ] 測試備份與恢復
- [ ] 記錄所有憑證和配置

---

## 🔗 相關文檔

- [硬體需求指南](HARDWARE_REQUIREMENTS.md)
- [本地 AI 設置](LOCAL_AI_GUIDE.md)
- [直播配置指南](STREAMING_GUIDE.md)
- [系統架構](ARCHITECTURE.md)

---

## 📧 獲取幫助

如果部署遇到問題：

1. 查看 [GitHub Issues](https://github.com/RainesTaiwan/Project-Observer/issues)
2. 參考故障排除章節
3. 提交新的 Issue（附上詳細日誌）

---

**祝你部署順利！🚀**
