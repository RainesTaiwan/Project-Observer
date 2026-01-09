FROM node:18-slim

# 安裝 Python 和必要的系統依賴
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg-dev \
    libgif-dev \
    librsvg2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 複製 package.json 並安裝 Node.js 依賴
COPY package*.json ./
RUN npm install

# 複製 Python 依賴並安裝
COPY requirements.txt ./
    RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt
COPY . .

# 創建必要的目錄
RUN mkdir -p /app/skills /app/logs /app/memory

# 設置環境變量
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

CMD ["python3", "main.py"]
