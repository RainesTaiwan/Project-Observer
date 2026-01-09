#!/bin/bash
# 恢復備份腳本
# 使用方法: ./restore.sh /path/to/backup

set -e

BACKUP_PATH=$1
PROJECT_NAME="project-observer"

# 顏色輸出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$BACKUP_PATH" ]; then
    echo -e "${RED}❌ 錯誤: 請指定備份路徑${NC}"
    echo ""
    echo "使用方法:"
    echo "  ./restore.sh /path/to/backup"
    echo ""
    echo "可用的備份:"
    ls -ld backups/backup_* 2>/dev/null || echo "  (無可用備份)"
    exit 1
fi

if [ ! -d "$BACKUP_PATH" ]; then
    echo -e "${RED}❌ 錯誤: 備份目錄不存在: $BACKUP_PATH${NC}"
    exit 1
fi

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Project Observer 恢復工具${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "${YELLOW}⚠️  警告: 此操作將覆蓋當前數據！${NC}"
echo -e "備份路徑: ${BLUE}$BACKUP_PATH${NC}"
echo ""

# 顯示備份資訊
if [ -f "$BACKUP_PATH/backup_info.txt" ]; then
    echo -e "${BLUE}備份資訊:${NC}"
    cat "$BACKUP_PATH/backup_info.txt"
    echo ""
fi

# 確認操作
read -p "確定要恢復此備份嗎? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}❌ 操作已取消${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🔄 開始恢復...${NC}"

# 1. 停止所有容器
echo -e "${BLUE}⏸️  停止容器...${NC}"
docker-compose down
echo -e "${GREEN}✅ 容器已停止${NC}"

# 函數：恢復 Docker Volume
restore_volume() {
    local volume_name=$1
    local backup_file=$2
    
    if [ ! -f "$BACKUP_PATH/$backup_file" ]; then
        echo -e "${YELLOW}⚠️  跳過 $backup_file (文件不存在)${NC}"
        return 0
    fi
    
    echo -e "${BLUE}📦 恢復 $backup_file...${NC}"
    
    # 刪除舊 volume（如果存在）
    docker volume rm ${PROJECT_NAME}_${volume_name} 2>/dev/null || true
    
    # 創建新 volume
    docker volume create ${PROJECT_NAME}_${volume_name}
    
    # 恢復數據
    docker run --rm \
        -v ${PROJECT_NAME}_${volume_name}:/data \
        -v "$(cd "$BACKUP_PATH" && pwd)":/backup \
        alpine sh -c "cd /data && tar xzf /backup/$backup_file"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $backup_file 恢復完成${NC}"
    else
        echo -e "${RED}❌ $backup_file 恢復失敗${NC}"
        return 1
    fi
}

# 2. 恢復各個 Volume
restore_volume "mc-data" "minecraft-world.tar.gz"
restore_volume "chroma-data" "chromadb.tar.gz"
restore_volume "agent-skills" "ai-skills.tar.gz"
restore_volume "agent-logs" "ai-logs.tar.gz"
restore_volume "agent-memory" "ai-memory.tar.gz"

# 3. 恢復配置文件
echo -e "${BLUE}📦 恢復配置文件...${NC}"

if [ -f "$BACKUP_PATH/.env" ]; then
    cp "$BACKUP_PATH/.env" .env
    echo -e "${GREEN}✅ .env 已恢復${NC}"
else
    echo -e "${YELLOW}⚠️  .env 不存在於備份中，跳過${NC}"
fi

if [ -f "$BACKUP_PATH/docker-compose.yml" ]; then
    # 備份當前的 docker-compose.yml
    if [ -f "docker-compose.yml" ]; then
        cp docker-compose.yml docker-compose.yml.before-restore
        echo -e "${BLUE}💾 當前 docker-compose.yml 已備份為 docker-compose.yml.before-restore${NC}"
    fi
    
    read -p "是否恢復 docker-compose.yml? (yes/no): " restore_compose
    if [ "$restore_compose" = "yes" ]; then
        cp "$BACKUP_PATH/docker-compose.yml" docker-compose.yml
        echo -e "${GREEN}✅ docker-compose.yml 已恢復${NC}"
    else
        echo -e "${YELLOW}⏭️  跳過 docker-compose.yml${NC}"
    fi
fi

# 4. 重啟服務
echo ""
echo -e "${BLUE}🚀 重啟服務...${NC}"
docker-compose up -d

# 5. 等待服務啟動
echo -e "${BLUE}⏳ 等待服務啟動...${NC}"
sleep 10

# 6. 檢查服務狀態
echo ""
echo -e "${BLUE}檢查服務狀態:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}✅ 恢復完成！${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${BLUE}💡 後續步驟:${NC}"
echo "  1. 檢查服務狀態: docker-compose ps"
echo "  2. 查看日誌: docker-compose logs -f"
echo "  3. 訪問 Dashboard: http://localhost:8501"
echo "  4. 連接 Minecraft: localhost:25565"
echo ""
