#!/bin/bash
# 自動備份腳本
# 使用方法: ./backup.sh

set -e

BACKUP_DIR="${BACKUP_DIR:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$DATE"
PROJECT_NAME="project-observer"

# 顏色輸出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Project Observer 備份工具${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 創建備份目錄
mkdir -p "$BACKUP_PATH"
echo -e "${GREEN}📁 創建備份目錄: $BACKUP_PATH${NC}"

# 函數：備份 Docker Volume
backup_volume() {
    local volume_name=$1
    local backup_name=$2
    
    echo -e "${BLUE}📦 備份 $backup_name...${NC}"
    
    docker run --rm \
        -v ${PROJECT_NAME}_${volume_name}:/data \
        -v "$(pwd)/$BACKUP_PATH":/backup \
        alpine tar czf /backup/${backup_name}.tar.gz -C /data .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $backup_name 備份完成${NC}"
    else
        echo -e "${RED}❌ $backup_name 備份失敗${NC}"
        return 1
    fi
}

# 1. 備份 Minecraft 世界
backup_volume "mc-data" "minecraft-world"

# 2. 備份 ChromaDB
backup_volume "chroma-data" "chromadb"

# 3. 備份 AI 技能
backup_volume "agent-skills" "ai-skills"

# 4. 備份日誌
backup_volume "agent-logs" "ai-logs"

# 5. 備份記憶庫
backup_volume "agent-memory" "ai-memory"

# 6. 備份配置文件
echo -e "${BLUE}📦 備份配置文件...${NC}"
cp .env "$BACKUP_PATH/.env" 2>/dev/null || echo "警告: .env 不存在"
cp docker-compose.yml "$BACKUP_PATH/" 2>/dev/null
cp docker-compose.prod.yml "$BACKUP_PATH/" 2>/dev/null || true

# 7. 創建備份資訊文件
cat > "$BACKUP_PATH/backup_info.txt" << EOF
備份資訊
========================================
備份時間: $(date)
專案名稱: $PROJECT_NAME
主機名稱: $(hostname)
Docker 版本: $(docker --version)
========================================

容器狀態:
$(docker-compose ps 2>/dev/null || echo "無法獲取容器狀態")

========================================

磁碟空間:
$(df -h 2>/dev/null | grep -E '^/dev/')

========================================
EOF

echo -e "${GREEN}✅ 備份資訊文件已創建${NC}"

# 8. 計算備份大小
BACKUP_SIZE=$(du -sh "$BACKUP_PATH" | cut -f1)
echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}✅ 備份完成！${NC}"
echo -e "${GREEN}======================================${NC}"
echo -e "備份位置: ${BLUE}$BACKUP_PATH${NC}"
echo -e "備份大小: ${BLUE}$BACKUP_SIZE${NC}"
echo ""

# 9. 列出備份內容
echo -e "${BLUE}備份內容:${NC}"
ls -lh "$BACKUP_PATH"
echo ""

# 10. 清理舊備份（保留最近 7 個）
BACKUP_COUNT=$(ls -1d "$BACKUP_DIR"/backup_* 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 7 ]; then
    echo -e "${BLUE}🧹 清理舊備份（保留最近 7 個）...${NC}"
    ls -1td "$BACKUP_DIR"/backup_* | tail -n +8 | xargs rm -rf
    echo -e "${GREEN}✅ 已清理 $((BACKUP_COUNT - 7)) 個舊備份${NC}"
fi

# 11. 可選：上傳到雲端
if command -v rclone &> /dev/null && [ ! -z "$RCLONE_REMOTE" ]; then
    echo -e "${BLUE}☁️  上傳到雲端: $RCLONE_REMOTE${NC}"
    rclone copy "$BACKUP_PATH" "$RCLONE_REMOTE:backups/$(basename $BACKUP_PATH)" --progress
    echo -e "${GREEN}✅ 雲端上傳完成${NC}"
fi

echo ""
echo -e "${GREEN}💡 恢復方法:${NC}"
echo -e "   ./restore.sh $BACKUP_PATH"
echo ""
